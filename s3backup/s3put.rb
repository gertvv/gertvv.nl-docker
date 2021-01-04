#!/usr/bin/env ruby
require 'rubygems'
require 'bundler/setup'

require 'aws-sdk-v1'
require 'openssl'

key = ARGV[0]
bucket = ARGV[1] 

# use `ssh-keygen -m pem` to generate
pkey = OpenSSL::PKey::RSA.new(File.read('rsa_key'), ENV['RSA_KEY_PASSPHRASE'])

s3_object = AWS.s3.buckets[bucket].objects[key]
s3_object.write({:file => key, :encryption_key => pkey})
