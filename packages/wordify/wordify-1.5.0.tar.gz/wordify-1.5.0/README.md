# wordify
Wordify is a Python class that converts a given number into its word representation. It can convert numbers up to centillions.

## Usage

1. From `converter` import the needed class (you have `IntegerConverter` and `DecimalConverter`)
   ```python
   from wordify.converter import IntegerConverter
   from wordify.converter import DecimalConverter
   ```

2. Create an instance of the `Converter` class by providing a number to be converted.
   ```python
   int_number = 12345
   int_converter = IntegerConverter(int_number)
   dec_number = 123.45
   dec_converter = DecimalConverter(dec_number)
   ```

3. Convert the number to its word representation using the `convert` method.
   ```python
   int_word_representation = int_converter.convert()
   dec_word_representation = dec_converter.convert()
   ```

4. Print the word representation.
   ```python
    print(int_word_representation)  # output: twelve thousand and three hundred forty five
    print(dec_word_representation)  # output: one hundred twenty three point four five
   ```

## Example

```python
from converter import IntegerConverter

# Create a Converter instance with a number
number = 12345
converter = IntegerConverter(number)

# Convert the number to words
word_representation = converter.convert()

# Print the word representation
print(word_representation)   # output: twelve thousand and three hundred forty five
```

## Customization

You can set a new number for conversion using the `set_number` method.
   ```python
   converter.set_number(98765)
   ```
After setting the new number, you need to call the `convert` method again to obtain the word representation.

## License

The code in this repository is licensed under the MIT License.

You can find the full text of the license in the [LICENSE](https://github.com/fathiabdelmalek/wordify/blob/main/LICENSE) file. For more information, please visit the repository on [GitHub](https://github.com/fathiabdelmalek/wordify).