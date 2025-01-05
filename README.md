<div align="center">

![kun-mini](/static/images/hexagrams/mini/white/02.png)

</div>


# I Ching Static Page Generator.

This project is a static site generated from scraping [i-ching online](https://www.iching-online.com). 
You can create your own page and read each hexagram. (Basically is a web book).

To run this project you can use the bash scripts. (run the `-h` tag for help)

## Use:

```
./python_env.sh
./scraper.sh --raw_html
./html_to_md.sh
./main.sh
```

After running main, you will be able to access port `:42069` and check the I Ching

> [!WARNING]
> Maybe you will need a `.env` file with some information for the download to work properly. For me it was working without.
> 
> ```txt
> COOKIE=<your cookie>
> ```

## TODO:

- [ ] Finish the CSS
- [ ] Landing Page:
    - [ ] Create the JavaScript calculator for hexagrams:
        - [ ] Create Form for the `html`
        - [ ] Create the script for the `html`
    - [ ] Create the hexagram box with the `mini` images
- [ ] Builder from html raw:
    - [ ] Add the `<a>` tag to the recursive function
    - [ ] Add the links from one hexagram to another (probably need a map for this)
    - [ ] Add the link to triagram from hexagram
- [ ] Static page generator:
    - [ ] Add `form` tag to to `ParentNode`. This include `<id>`
    - [ ] Add `script` tag to `ParentNode`
    - [ ] Update the `helper_block_to_html` to include `form` and `script`
