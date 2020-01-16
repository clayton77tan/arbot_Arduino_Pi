#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <termios.h>
#include <wiringPi.h>
#include <errno.h>
#include <libusb.h>

int main (int argc, char * argv[]){
	wiringPiSetup();
	libusb_device_handle* USB;
	unsigned char sent[64];
	int sent_B;
	int rebound;

	libusb_init(NULL);
	USB = libusb_open_device_with_vid_pid(NULL, 0x04B4, 0x8051);

	if(USB == NULL){
		perror("device not found\n");
	}
	if(libusb_reset_device(USB) <= 0){
		perror("Device reset failed\n");
	}

	if(libusb_set_configuration(USB, 1) <= 0){
		perror("Set configuration failed\n");
	}
	if(libusb_claim_interface(USB,0) <= 0){
		perror("Cannot claim interface");
	}

	for(int i = 0; i < 64; i++){
		sent[i] = i;
	}
	
	while(1){
		rebound = libusb_bulk_transfer(USB, 0x02,sent, 64, &sent_B, 0);
		if(rebound == 0){
		
		}else {
			exit(1);
		}
	}
	libusb_close(USB);
}
