-- Restructure the print manuscript (docx) for a reflowable Kindle ebook.
--  * drop the printed "Contents" (page numbers) and the ISBN placeholder line
--  * title page + copyright page styled from the opening paragraphs
--  * "PART I THE IPP PARADOX" running markers -> one part heading per part
--  * "Chapter N [Test k: X]" label + H1 -> H2 "N. Title" with a small kicker
--  * inside parts, every other heading moves down one level (nested TOC)

local stringify = pandoc.utils.stringify

local PARTS = {
  ["PART I THE IPP PARADOX"] = "Part I · The IPP Paradox",
  ["PART II THE SEVEN TESTS"] = "Part II · The Seven Tests",
  ["PART III FROM TESTS TO DECISIONS"] = "Part III · From Tests to Decisions",
  ["CONCLUSION"] = "Conclusion",
  ["APPENDICES"] = "Appendices",
}

local function text(b) return stringify(b):gsub("^%s+", ""):gsub("%s+$", "") end

function Pandoc(doc)
  local out = {}
  local blocks = doc.blocks
  local i = 1
  local n = #blocks
  local skipping = false      -- inside the printed Contents
  local in_parts = false      -- demote headings once parts begin
  local current_part = nil
  local front = {}            -- blocks before the first heading
  local seen_heading = false
  local removed_isbn = 0

  while i <= n do
    local b = blocks[i]
    local t = (b.t == "Para" or b.t == "Plain") and text(b) or nil

    if b.t == "Header" then seen_heading = true end

    -- the printed table of contents: from "Contents" to the next level-1 heading
    if b.t == "Header" and b.level == 1 and text(b) == "Contents" then
      skipping = true
      i = i + 1
      goto continue
    end
    if skipping then
      if b.t == "Header" and b.level == 1 then skipping = false else i = i + 1; goto continue end
    end

    if t and t:find("[ISBN, paperback]", 1, true) then
      -- ebook: drop the placeholder (KDP assigns an ASIN); print: BOOK_ISBN replaces it
      removed_isbn = removed_isbn + 1
      local isbn = os.getenv("BOOK_ISBN")
      if isbn and isbn ~= "" then
        table.insert(front, pandoc.Para(pandoc.Str("ISBN " .. isbn .. " (paperback)")))
      end
      i = i + 1
      goto continue
    end

    if not seen_heading then
      table.insert(front, b)
      i = i + 1
      goto continue
    end

    -- part marker, optionally followed by a chapter/appendix label, then the H1
    if t and PARTS[t] then
      if PARTS[t] ~= current_part then
        current_part = PARTS[t]
        in_parts = true
        local h = pandoc.Header(1, pandoc.Str(current_part), pandoc.Attr("", {"part"}))
        table.insert(out, h)
      end
      i = i + 1
      goto continue
    end

    if in_parts and t and (t:match("^Chapter %d+") or t:match("^Appendix %u$") or t == "Conclusion") then
      local nxt = blocks[i + 1]
      if nxt and nxt.t == "Header" and nxt.level == 1 then
        local title = text(nxt)
        local num = t:match("^Chapter (%d+)")
        local app = t:match("^Appendix (%u)$")
        local label = t
        if num then
          title = num .. ". " .. title
          local rest = t:match("^Chapter %d+%s+(.+)$")
          label = "Chapter " .. num .. (rest and (" · " .. rest) or "")
        elseif app then
          title = "Appendix " .. app .. ". " .. title
        end
        table.insert(out, pandoc.Header(2, pandoc.Str(title), pandoc.Attr(nxt.identifier, {"chapter"})))
        -- keep the label only where it adds something to the title ("Chapter 4 · Test 1: Need")
        if label:find(" · ", 1, true) then
          table.insert(out, pandoc.Div({pandoc.Para(pandoc.Str(label))}, pandoc.Attr("", {"kicker"})))
        end
        -- the byline repeated under every chapter title in the print layout
        local after = blocks[i + 2]
        if after and after.t == "Para" and text(after) == "Emmanuel Boujieka Kamga" then
          table.insert(out, pandoc.Div({after}, pandoc.Attr("", {"byline"})))
          i = i + 3
        else
          i = i + 2
        end
        goto continue
      end
    end

    if b.t == "Header" then
      if b.level == 1 and in_parts then
        -- a level-1 heading with no part/chapter label ends the parts (About the Author)
        in_parts = false
        current_part = nil
      elseif in_parts then
        b.level = math.min(b.level + 1, 6)
      end
    end
    table.insert(out, b)
    i = i + 1
    ::continue::
  end

  -- title page and copyright page from the opening paragraphs
  local title_blocks, copy_blocks = {}, {}
  local in_copy = false
  for _, b in ipairs(front) do
    if not in_copy and stringify(b):find("Copyright", 1, true) then in_copy = true end
    table.insert(in_copy and copy_blocks or title_blocks, b)
  end
  -- each gets its own hidden, unlisted heading so pandoc does not add a visible book-title heading
  local function hidden(txt, id) return pandoc.Header(1, pandoc.Str(txt), pandoc.Attr(id, {"unnumbered", "unlisted", "hidden"})) end
  local head = {}
  if #title_blocks > 0 then
    table.insert(head, hidden("Title Page", "title-page"))
    table.insert(head, pandoc.Div(title_blocks, pandoc.Attr("", {"titlepage"})))
  end
  if #copy_blocks > 0 then
    table.insert(head, hidden("Copyright", "copyright-page"))
    table.insert(head, pandoc.Div(copy_blocks, pandoc.Attr("", {"copyright"})))
  end
  for k = #head, 1, -1 do table.insert(out, 1, head[k]) end

  io.stderr:write(string.format("kindle.lua: removed ISBN lines=%d, blocks=%d\n", removed_isbn, #out))
  doc.blocks = out
  return doc
end
