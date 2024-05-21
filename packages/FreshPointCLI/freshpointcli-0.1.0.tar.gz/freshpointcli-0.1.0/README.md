
# FreshPointCLI
A CLI REPL interface to query FreshPoint product price and availability.

## Installation

`FreshPointCLI` supports Python 3.8 and higher. The library can be installed
using the following CLI command:

```console
$ pip install freshpointcli
```

## Usage

`FreshPointCLI` is a Read-Eval-Print Loop (REPL) application intended to be used
only from the command line interface (CLI).

### Starting Up the Application

You can initialize the application
using the following CLI command:

```console
$ freshpoint <location_id>
```
*<location_id>* is the ID of the FreshPoint location to track. It can be found
in the page URL. For example, for https://my.freshpoint.cz/device/product-list/296,
location id is *296*.

Location ID is preserved between the application sessions, so if you intend
to track the same location as the last time, you can omit the location id
argument and invoke the application without it.

Invoke the application with `--help` to receice start-up information:

```console
$ freshpoint --help
```

### Querying the Product Page

Once the application is running, it displays an input promt, and you can type in
queries to check for products' availability, price, and more. 

To query if a product is avalable, use the following command:

```console
FreshPoint@LocationName> <product_name> --available
```

Replace `<product_name>` with the name of the product you want to query. Note
that name and category matching is case-insensitive, supports partial match,
and ignores diacritics.

To query for all the products that are currently on sale, use the following
command:

```console
FreshPoint@LocationName> --sale
```

Query arguments can be combined in any way:

```console
FreshPoint@LocationName> --available --price-max 100 --vegerarian
```

To display all the supported arguments, use `--help`:

```console
FreshPoint@LocationName> --help
```

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please
open an issue on GitHub. If you would like to contribute code, please fork
the repository and submit a pull request.

## License

`FreshPointCLI` is licensed under the MIT License.
See the `LICENSE` file for more information.
