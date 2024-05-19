# Probability-Distribution-Devin

A Python package for Gaussian and Binomial probability distributions.

## Installation

Run the following to install:

```bash
pip install Probability-Distribution-Devin
```

## Usage

```python
from Probability-Distribution-Devin import Gaussian, Binomial

# Create Gaussian and Binomial objects
gaussian = Gaussian(10, 7)
binomial = Binomial(0.4, 20)

# Calculate mean and standard deviation
print(gaussian.mean)
print(binomial.standard_deviation)
```

## Development

For development, you can use virtualenv to create an isolated Python environment.

```bash
virtualenv venv
source venv/bin/activate
```

Install `Probability-Distribution-Devin` in editable mode with:

```bash
pip install -e .
```

## Testing

To run tests, install the package and run:

```bash
python -m unittest discover
```

## License

MIT
