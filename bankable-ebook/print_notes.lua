-- Print: footnotes become inline spans that the stylesheet floats to the page foot.
function Note(el)
  return pandoc.Span(pandoc.utils.blocks_to_inlines(el.content, {pandoc.Space()}), pandoc.Attr("", {"fn"}))
end
