#!/usr/bin/env ruby
require 'rubygems'
require 'bundler/setup'

require 'aws-sdk-v1'
require 'openssl'

key = ARGV[0]
bucket = ARGV[1] 

# use `ssh-keygen -m pem` to generate
pkey = OpenSSL::PKey::RSA.new(File.read("#{__dir__}/rsa_key"), ENV['RSA_KEY_PASSPHRASE'])

s3_object = AWS.s3.buckets[bucket].objects[key]
File.open(key, 'wb') do |file|
  s3_object.read({ :encryption_key => pkey }) do |chunk|
    file.write(chunk)
  end
end
