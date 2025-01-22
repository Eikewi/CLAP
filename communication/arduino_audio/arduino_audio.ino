#include <PDM.h>
#include <CLAP_inferencing.h>


// If your target is limited in memory remove this macro to save 10K RAM
#define EIDSP_QUANTIZE_FILTERBANK   0

/**
   Define the number of slices per model window. E.g. a model window of 1000 ms
   with slices per model window set to 4. Results in a slice size of 250 ms.
   For more info: https://docs.edgeimpulse.com/docs/continuous-audio-sampling
*/
#define EI_CLASSIFIER_SLICES_PER_MODEL_WINDOW 4
#define SHOW_RESULTS false
#define STREAM_BUFFER_SIZE 1000
#define CLASSIFICATION_CONFIDENCE_THRESHOLD 0.8

/** Audio buffers, pointers and selectors */
typedef struct {
  signed short *buffers[2];
  unsigned char buf_select;
  unsigned char buf_ready;
  unsigned int buf_count;
  unsigned int n_samples;
} inference_t;

static inference_t inference;
static bool record_ready = false;
static signed short *inferenceSampleBuffer;
static bool debug_nn = false; // Set this to true to see e.g. features generated from the raw signal
static int print_results = -(EI_CLASSIFIER_SLICES_PER_MODEL_WINDOW);

const char* keywords[] = {"Clap", "Word"};
const size_t keywords_length = sizeof(keywords) / sizeof(keywords[0]);

static short streamSampleBuffer[STREAM_BUFFER_SIZE];
static volatile int streamSamplesRead = 0;

enum State {
  START_KEYWORD_DETECTION, // Clear buffers and freshly start ww detection
  KEYWORD_DETECTION, // Run ww detection
  AUDIO_STOPPED, // Wait until we can either stream audio or go to ww detection
  STREAM_AUDIO // Send audio via serial
};
static State currentState;
static bool stream_pdm_running = false;
static bool inference_pdm_running = false;

void setup() {
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_BLUE, OUTPUT);
  currentState = AUDIO_STOPPED;
  Serial.begin(115200);
  while (!Serial);

  run_classifier_init();
}

void changeStateOnInput() {
  int incomingByte = 0;
  // Read input and change state
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    // Change state if the python script tells us to do so
    if (incomingByte == 1 || incomingByte == (int) '1') {
      currentState = AUDIO_STOPPED;
    } else if (incomingByte == 2 || incomingByte == (int) '2') {
      currentState = START_KEYWORD_DETECTION;
    }
  }
}

void loop() {
  changeStateOnInput();

  if (currentState == START_KEYWORD_DETECTION) {
    setLED(false, true, false);
    // Clean up from audio streaming, initialize buffers and start ww detection

    if (stream_pdm_running) {
      stream_pdm_end();
    }

    // Starting pdm for inference if it is not running yet
    if (!inference_pdm_running && !inference_pdm_start(EI_CLASSIFIER_SLICE_SIZE)) {
      ei_printf("ERR: Could not allocate audio buffer (size %d), this could be due to the window length of your model\r\n", EI_CLASSIFIER_RAW_SAMPLE_COUNT);
      return;
    }

    // Classify the first chunk of audio
    if (classify()) {
      currentState = STREAM_AUDIO;
      inference_pdm_end();
      stream_pdm_start();
    } else {
      // All the initialization work is done, so we can change to the standard keyword spotting case
      currentState = KEYWORD_DETECTION;
    }
  } else if (currentState == KEYWORD_DETECTION) {
    setLED(false, true, false);
    // Try to detect keywords
    if (classify()) {
      currentState = STREAM_AUDIO;
      inference_pdm_end();
      stream_pdm_start();
    }
  } else if (currentState == STREAM_AUDIO) {
    setLED(true, false, false);
    // Stream available audio via serial port
    if (streamSamplesRead > 0) {
      // Daten paketweise senden
      Serial.write((const uint8_t*)streamSampleBuffer, streamSamplesRead * sizeof(short));
      streamSamplesRead = 0;
    }
  } else if (currentState == AUDIO_STOPPED) {
    setLED(false, false, true);
    // Stop all audio
    if (inference_pdm_running) {
      inference_pdm_end();
    }
    stream_pdm_end();
  }

}

/**
   @brief     Records audio and classifies using the neural network.

   @return    True, if "Clap" or "Word" is the most likely label, false otherwise.
*/
static bool classify() {
  // Record some audio for classification
  bool m = inference_pdm_record();
  if (!m) {
    ei_printf("ERR: Failed to record audio...\n");
    return false;
  }

  // Fill objects for classifier-library-function
  signal_t signal;
  signal.total_length = EI_CLASSIFIER_SLICE_SIZE;
  signal.get_data = &microphone_audio_signal_get_data;
  ei_impulse_result_t result = {0};

  // Run classifier
  EI_IMPULSE_ERROR r = run_classifier_continuous(&signal, &result, debug_nn);

  if (r != EI_IMPULSE_OK) {
    ei_printf("ERR: Failed to run classifier (%d)\n", r);
    return false;
  }

  if (++print_results >= (EI_CLASSIFIER_SLICES_PER_MODEL_WINDOW)) {
    // print the predictions
    if (SHOW_RESULTS) {
      ei_printf("Predictions ");
      ei_printf("(DSP: %d ms., Classification: %d ms.)",
              result.timing.dsp, result.timing.classification);
      ei_printf(": \n");
    }
   
    for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++) {
      if (SHOW_RESULTS) {
        ei_printf("    %s: %.5f\n", result.classification[ix].label,
                  result.classification[ix].value);
      }
      if (isKeyword(result.classification[ix].label) && result.classification[ix].value > CLASSIFICATION_CONFIDENCE_THRESHOLD) {
        return true;
      }
    }

    print_results = 0;
  }
  return false;
}

static bool isKeyword(const char* label) {
  for (uint8_t i = 0; i < keywords_length; i++) {
    if (strcmp(keywords[i], label) == 0) {
      return true;
    }
  }
  return false;
}

/**
   @brief Starts the PDM for the audio stream via the Serial port.
*/
void stream_pdm_start() {
  PDM.onReceive(stream_pdm_data_callback);
  PDM.setBufferSize(STREAM_BUFFER_SIZE * sizeof(short));
  PDM.setGain(20);
  if (!PDM.begin(1, 16000)) {
    Serial.println("PDM-Microphone couldn't be started!");
    while (1);
  }
  stream_pdm_running = true;
}

/**
   @brief On-Receive-Callback for the PDM for the audio stream mode.
*/
void stream_pdm_data_callback() {
  int bytesAvailable = PDM.available();
  PDM.read(streamSampleBuffer, bytesAvailable);
  streamSamplesRead = bytesAvailable / 2;
}

/**
   @brief Ends the PDM for the audio stream mode.
*/
void stream_pdm_end() {
  streamSamplesRead = 0;
  PDM.end();
  stream_pdm_running = false;
}

/**
   @brief      Init inferencing struct and setup/start PDM

   @param[in]  n_samples  The n samples

   @return     { description_of_the_return_value }
*/
static bool inference_pdm_start(uint32_t n_samples)
{
  inference.buffers[0] = (signed short *)calloc(n_samples, sizeof(signed short));

  if (inference.buffers[0] == NULL) {
    return false;
  }

  inference.buffers[1] = (signed short *)calloc(n_samples, sizeof(signed short));

  if (inference.buffers[1] == NULL) {
    free(inference.buffers[0]);
    return false;
  }

  inferenceSampleBuffer = (signed short *)calloc((n_samples >> 1), sizeof(signed short));

  if (inferenceSampleBuffer == NULL) {
    free(inference.buffers[0]);
    free(inference.buffers[1]);
    return false;
  }

  inference.buf_select = 0;
  inference.buf_count = 0;
  inference.n_samples = n_samples;
  inference.buf_ready = 0;

  // configure the data receive callback
  PDM.onReceive(inference_pdm_data_callback);

  PDM.setBufferSize((n_samples >> 1) * sizeof(int16_t));

  // initialize PDM with:
  // - one channel (mono mode)
  // - a 16 kHz sample rate
  // We need to manually downsample, as the microphone won't start with 8kHz sampling rate.
  if (!PDM.begin(1, 2 * EI_CLASSIFIER_FREQUENCY)) {
    ei_printf("Failed to start PDM!");
  }

  // set the gain, defaults to 20
  PDM.setGain(127);

  record_ready = true;
  inference_pdm_running = true;

  return true;
}

/**
   @brief On-Receive-Callback for the inference mode.
*/
void inference_pdm_data_callback() {
  int bytesAvailable = PDM.available();
  // read into the sample buffer
  int bytesRead = PDM.read((char *)&inferenceSampleBuffer[0], bytesAvailable);

  if (record_ready) {
    // taking steps of two to do the downsampling from 16kHz to 8kHz
    for (int i = 0; i<bytesRead >> 1; i += 2) {
      inference.buffers[inference.buf_select][inference.buf_count++] = inferenceSampleBuffer[i];

      if (inference.buf_count >= inference.n_samples) {
        inference.buf_select ^= 1;
        inference.buf_count = 0;
        inference.buf_ready = 1;
      }
    }
  }
}

/**
   @brief      Wait on new data

   @return     True when finished
*/
static bool inference_pdm_record(void)
{
  bool ret = true;

  if (inference.buf_ready == 1) {
    ei_printf(
      "Error sample buffer overrun. Decrease the number of slices per model window "
      "(EI_CLASSIFIER_SLICES_PER_MODEL_WINDOW)\n");
    ret = false;
  }
  while (inference.buf_ready == 0) {
    delay(1);
  }
  inference.buf_ready = 0;

  return ret;
}

/**
   @brief      Stop PDM and release buffers
*/
static void inference_pdm_end(void)
{
  PDM.end();
  free(inference.buffers[0]);
  free(inference.buffers[1]);
  free(inferenceSampleBuffer);
  inference_pdm_running = false;
}

/**
   Get raw audio signal data
*/
static int microphone_audio_signal_get_data(size_t offset, size_t length, float *out_ptr)
{
  numpy::int16_to_float(&inference.buffers[inference.buf_select ^ 1][offset], out_ptr, length);

  return 0;
}

static void setLED(bool red, bool green, bool blue) {
  digitalWrite(LED_RED, !red ? HIGH : LOW);
  digitalWrite(LED_GREEN, !green ? HIGH : LOW);
  digitalWrite(LED_BLUE, !blue ? HIGH : LOW);
}


#if !defined(EI_CLASSIFIER_SENSOR) || EI_CLASSIFIER_SENSOR != EI_CLASSIFIER_SENSOR_MICROPHONE
#error "Invalid model for current sensor."
#endif
