# 
`docker run --rm --volume "$(pwd):/data" pandoc/latex -s sample.tex -o sample.text`

`docker run --rm --volume "$(pwd):/data" pandoc/latex -s sample.text -o sample.pdf`


### references
> https://tectonic-typesetting.github.io/ - A rust client for latex, docker friendly
