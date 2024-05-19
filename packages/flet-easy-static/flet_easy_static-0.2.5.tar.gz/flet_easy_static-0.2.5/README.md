<div align="center">
    <img src="https://github.com/Daxexs/flet-easy/blob/main/media/logo.png?raw=true" alt="logo" width="250">
</div>


# 🔥Flet-Easy (Flet-Easy-Static)
`Flet-Easy` is a package built as an add-on for [`Flet`](https://github.com/flet-dev/flet), designed for beginners what it does is to make `Flet` easier when building your apps, with a tidier and simpler code.

# Modification 
`Flet-Easy-Static` is a modification of `Flet-Easy` that allows you to create and publish your `Flet-Easy` project as a static pyodide website
### As a result, the following features are not available:
- Export As AGSI Application is removed (This was the limiting factor for creating a static website since it is not available in the flet-pyodide package)
- FastAPI Integration is removed (This was the limiting factor for creating a static website since it is not available in the flet-pyodide package)
- Removed `flet` as a required dependency since `flet-pyodide` is used in the web not the `flet` package
- Added `PyJWT` `rsa` `ssl` `parse` as a requirement since it not included in pyodide environment
### How To Use:
- Add `flet-easy-static` to your project `requirements.txt`
- How To Import Package:
```python
# Method 1: Importing the package as fs in your project (Disadvantage: You will have to import this in you whole project, and also install the package)
import flet_easy_static as fs
# Method 2: Check if the platform is emscripten and import the package accordingly (Disadvantage: You will have to import this in you whole project)
# This method is useful if you want to run the same code on both the desktop and the web and you don't have to install flet-easy-static package on your desktop
if sys.platform == "emscripten":  # Check if in Pyodide environment
    import flet_easy_static as fs
else:
    import flet_easy as fs
  ```
- Now you can safely run `flet publish` on your static website application
### 🔥 This pacakge is just a small modification of the original `Flet-Easy` package and all the credit goes to the original author [Daxexs](https://pypi.org/user/Daxexs/) 

## Features
* Easy to use (**hence the name**).
* Facilitates `flet` event handling.
* Simple page routing (There are three ways) for whichever one suits you best. ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/dynamic-routes/))
* App construction with numerous pages and custom flet configurations for desktop, mobile and web sites.
* Provides a better construction of your code, which can be scalable and easy to read (it adapts to your preferences, there are no limitations).
* Dynamic routing, customization in the routes for greater accuracy in sending data. ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/dynamic-routes/#custom-validation))
* Routing protection ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/Customized-app/Route-protection/))
* Custom Page 404 ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/Customized-app/Page-404/))
* Controlled data sharing between pages. ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/Data-sharing-between-pages/))
* Asynchronous support.
* Middleware Support (in the app in general and in each of the pages). ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/Midleware/))
* JWT support for authentication sessions in the data parameter. (useful to control the time of sessions) ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/Basic-JWT/))
* Working with other applications. ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/Data-sharing-between-pages/))
* CLI to create app structure `FletEasy` (`fs init`) ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/CLI-to-create-app/))
* Easy integration of `on_keyboard_event` in each of the pages. ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/Events/keyboard-event/))
* Use the percentage of the page width and height of the page with `on_resize`. ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/Events/On-resize/))
* `ResponsiveControlsy` control to make the app responsive, useful for desktop applications. ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/ResponsiveControlsy/))
* Soporta Application Packaging para su distribución. ([view](https://flet.dev/docs/publish))

## 📌Flet events it handles

- `on_route_change` :  Dynamic routing
- `on_view_pop`
- `on_keyboard_event`
- `on_resize`
- `on_error`

## 💻Installation:

Requires installation [`Flet`](https://github.com/flet-dev/flet) for use:
```bash
  pip install flet --upgrade
```
```bash
  pip install flet-easy-static
```

## 💻Update:
```bash
  pip install flet-easy-static --upgrade
```

## 🔥Flet-Easy app example
Here is an example of an application with 2 pages, "Home" and "Counter":

```python
import flet as ft
import flet_easy_static as fs

app = fs.FletEasy(route_init="/flet-easy")

# We add a page
@app.page(route="/flet-easy", title="Flet-Easy")
def index_page(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("Home page"),
            ft.FilledButton("Go to Counter", on_click=data.go("/counter")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

# We add a second page
@app.page(route="/counter", title="Counter")
def counter_page(data: fs.Datasy):
    page = data.page

    txt_number = ft.TextField(value="0", text_align="right", width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    return ft.View(
        controls=[
            ft.Row(
                [
                    ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                    txt_number,
                    ft.IconButton(ft.icons.ADD, on_click=plus_click),
                ],
                alignment="center",
            ),
            ft.FilledButton("Go to Home", on_click=data.go("/flet-easy")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

# We run the application
app.run()
```

## 🎬 **Mode**
![app example](https://github.com/Daxexs/flet-easy/blob/main/media/app-example.gif?raw=true "app example")

## 🚀 How to use `Flet-Easy`?
> [!IMPORTANT]
Documentation: https://daxexs.github.io/flet-easy/latest/

## 👀 Code examples
> [!NOTE]
https://github.com/Daxexs/flet-easy/tree/main/tests

## 🔎 Contribute to this project
Read the [CONTRIBUTING.md](https://github.com/Daxexs/flet-easy/blob/main/CONTRIBUTING.md) file

# 🧾 License
[Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/)