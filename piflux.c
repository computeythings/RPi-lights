#include <wiringPi.h>
#include <errno.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

#define SWITCH_PIN 26 // Pin to connect switch to
int pinState; // pin state (Defined after setup)

void toggleLights()
{
  int newState = digitalRead(SWITCH_PIN);
  if(newState) // if state reads 1 (HIGH)
    printf("Rising edge detected on %d with state %d\n", SWITCH_PIN, newState);
  else // if state reads 0 (LOW)
    printf("Falling edge detected on %d with state %d\n", SWITCH_PIN, newState);

  // Only run toggle script if current pin state is not the last logged state
  if(newState != pinState){
    // This is the actual script I use to toggle the lights
    system("./toggle-lights");
    pinState = newState;
  }
}

int main(void)
{
  printf("Starting wiringPi PiFlux\n");
  // pin setup
  if(wiringPiSetupGpio() < 0){
    fprintf(stderr, "Unable to setup wiringPi: %s\n", strerror(errno));
    return 1;
  }
  // initial pin state
  pinState = digitalRead(SWITCH_PIN);
  // Setup interrupt to toggle switches on any state change
  if(wiringPiISR(SWITCH_PIN, INT_EDGE_BOTH, &toggleLights) < 0) {
    fprintf(stderr, "Unable to setup ISR: %s\n", strerror(errno));
    return 1;
  }

  // Run until stopped
  while(1){
    delay(UINT_MAX);
  }

  return 0;
}
