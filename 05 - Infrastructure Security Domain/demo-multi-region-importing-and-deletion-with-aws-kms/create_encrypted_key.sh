#!/bin/bash

openssl pkeyutl \
    -in SooperDooperPlaintext.bin \
    -out SooperDooperEncryptedMaterial.bin \
    -inkey $CHANGE_ME \
    -keyform DER -pubin \
    -encrypt \
    -pkeyopt rsa_padding_mode:oaep \
    -pkeyopt rsa_oaep_md:sha1        