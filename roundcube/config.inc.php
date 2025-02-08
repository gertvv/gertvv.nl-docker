<?php

$config = [];

// Database connection string (DSN) for read+write operations
$config['db_dsnw'] = 'sqlite:////var/www/roundcube/db/sqlite.db?mode=0646';

$config['imap_host'] = 'ssl://mail.gertvv.nl';
$config['smtp_host'] = 'ssl://mail.gertvv.nl';
$config['smtp_user'] = '%u';
$config['smtp_pass'] = '%p';
$config['support_url'] = 'https://gertvv.nl/';
$config['product_name'] = 'gertvv.nl webmail';

// This key is used to encrypt the users imap password which is stored
// in the session record. For the default cipher method it must be
// exactly 24 characters long.
// YOUR KEY MUST BE DIFFERENT THAN THE SAMPLE VALUE FOR SECURITY REASONS
$config['des_key'] = 'rcmail-!24ByteDESkey*Str';

// List of active plugins (in plugins/ directory)
$config['plugins'] = [
    'archive',
    'zipdownload',
];

// skin name: folder from skins/
$config['skin'] = 'elastic';
