## Nextcloud Sync client for Sailfish OS

The library installs in `/usr/lib/nextcloud` for compatability with OwnCloud (which ships a library with the same name).
This means you will have to have that path in your `LD_LIBRARY_PATH` variable to use the client.
Like so:

    LD_LIBRARY_PATH="${LD_LIBRARY_PATH}":/usr/lib/nextcloud nextcloudcmd
    LD_LIBRARY_PATH="${LD_LIBRARY_PATH}":/usr/lib64/nextcloud nextcloudcmd

#### Credits

This build was inspired by and basically copied from SailSync ownCloud,
https://code.edin.io/edin/sailsync-owncloud

#### Compatability notes:

upstream version 2.6.4 is the only one suited for SailfishOS 4.x

  - support for Qt < 5.12 was dropped in commit 3867e73fd536a8f4b0e572e0281aa406a742a3a5
  - 2.6.5 uses qAsConst which is only in Qt 5.7

