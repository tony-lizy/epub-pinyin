# Deployment Guide for EPUB-Pinyin

This guide will help you deploy the epub-pinyin package to PyPI.

## Prerequisites

1. **PyPI Account**: You need a PyPI account to upload packages
   - Sign up at https://pypi.org/account/register/
   - Enable two-factor authentication (recommended)

2. **TestPyPI Account**: For testing before production deployment
   - Sign up at https://test.pypi.org/account/register/

3. **API Tokens**: Create API tokens for secure uploads
   - Go to your PyPI account settings
   - Create an API token with "Entire account" scope
   - Save the token securely

## Build Tools Installation

Install the required build tools:

```bash
pip install build twine
```

## Configuration

### 1. Create ~/.pypirc file

Create a configuration file for your PyPI credentials:

```bash
# Create the file
touch ~/.pypirc

# Edit the file with your credentials
nano ~/.pypirc
```

Add the following content (replace with your actual tokens):

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-actual-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-token-here
```

### 2. Alternative: Environment Variables

Instead of using ~/.pypirc, you can set environment variables:

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-actual-token-here
```

## Deployment Process

### Step 1: Build the Package

```bash
# Clean and build
python build_and_deploy.py
```

This will:
- Clean previous build artifacts
- Build the package (wheel and source distribution)
- Check the package for issues

### Step 2: Test on TestPyPI (Recommended)

First, test your package on TestPyPI:

```bash
python build_and_deploy.py --test
```

### Step 3: Test Installation from TestPyPI

```bash
# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ epub-pinyin

# Test the installation
python -c "import epub_pinyin; print('Installation successful!')"
```

### Step 4: Deploy to Production PyPI

If everything works on TestPyPI, deploy to production:

```bash
python build_and_deploy.py --upload
```

### Step 5: Verify Installation

```bash
# Install from production PyPI
pip install epub-pinyin

# Test the installation
python -c "import epub_pinyin; print('Production installation successful!')"
```

## Manual Deployment (Alternative)

If you prefer manual deployment:

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build package
python -m build

# Check package
twine check dist/*

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

## Version Management

### Updating Version

1. **Update version in setup.py**:
   ```python
   version="0.2.1",  # Increment version number
   ```

2. **Update version in pyproject.toml** (if using dynamic versioning):
   ```toml
   [project]
   dynamic = ["version"]
   ```

3. **Create a git tag** (recommended):
   ```bash
   git tag v0.2.1
   git push origin v0.2.1
   ```

### Version Numbering

Follow semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

## Troubleshooting

### Common Issues

1. **Authentication Errors**:
   - Check your ~/.pypirc file
   - Verify your API tokens
   - Ensure tokens have correct permissions

2. **Package Already Exists**:
   - Increment version number
   - Delete old versions from PyPI (if needed)

3. **Build Errors**:
   - Check for syntax errors in code
   - Verify all dependencies are listed in setup.py
   - Ensure MANIFEST.in includes all necessary files

4. **Import Errors After Installation**:
   - Check package structure
   - Verify __init__.py files
   - Test locally before uploading

### Package Size Issues

The package includes Chinese fonts, which makes it large (~50MB). This is normal and acceptable for PyPI.

## Security Best Practices

1. **Use API Tokens**: Never use username/password
2. **Two-Factor Authentication**: Enable on PyPI account
3. **Token Scope**: Use minimal required permissions
4. **Secure Storage**: Store tokens securely
5. **Regular Rotation**: Rotate tokens periodically

## Post-Deployment

After successful deployment:

1. **Update Documentation**: Update README.md if needed
2. **Create Release Notes**: Document changes
3. **Test Installation**: Test on different Python versions
4. **Monitor**: Check for user feedback and issues

## Continuous Integration

Consider setting up CI/CD for automated deployments:

```yaml
# Example GitHub Actions workflow
name: Deploy to PyPI
on:
  push:
    tags:
      - 'v*'
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install build twine
      - name: Build and publish
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: |
          python -m build
          twine upload dist/*
```

## Support

If you encounter issues:

1. Check PyPI documentation: https://packaging.python.org/
2. Review twine documentation: https://twine.readthedocs.io/
3. Check PyPI status: https://status.python.org/
4. Contact PyPI support if needed
