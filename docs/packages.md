# Holodeck Packages and Configuration
How packages are installed, managed, and interpreted in holodeck.

## Package Installation

Packages are located on an S3 bucket, due to the size of the files and the 
bandwidth required to distribute them. 

### Retrieving Package List
A version of holodeck has a certain set of packages that are associated with it. 
Each package can have multiple versions, and a version of holodeck can be 
compatible with multiple versions of a package. A package can also be added
after shipping a version of holodeck, so the client fetches a list of available
packages from the backend.

The client will post a GET to the following endpoint:
`%BACKEND%/packages/%HOLODECK_VERSION%/available`, or
`https://s3.amazonaws.com/holodeckworlds/packages/0.2.0/available` for example.

The server will return a JSON file with the following format:

```json
{
    "packages": {
        "%WORLD_NAME%" : ["%VERSION1", "%VERSION_2%"]
    }
}
```

for example

```json
{
    "packages": {
        "DefaultWorlds" : ["0.1.0", "0.1.1"],
        "MoveBox" : ["0.0.1"]
    }
}
```

The client will use this information to craft the download URL.

### Download URL

This is the format of a download URL:

`%BACKEND%/packages/%HOLODECK_VERSION%/%PACKAGE_NAME%/%PLATFORM%/%PACKAGE_VERSION%.zip`

for example

`%BACKEND%/packages/0.1.0/DefaultWorlds/Linux/1.0.2.zip`
