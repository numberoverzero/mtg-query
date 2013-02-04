def config_cloudinary(cloudinary, credentials_file):
    with open(credentials_file) as f:
        data = f.read()
    lines = data.split("\n")
    settings = {}
    for line in lines:
        key, value = line.split("=", 1)
        settings[key] = value
    cloudinary.config(**settings)
    return cloudinary
