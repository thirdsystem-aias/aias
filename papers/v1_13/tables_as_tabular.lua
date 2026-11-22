-- v1.13 Grounding Paper A copy (scripts/build_paper_v1_13.py) of papers/v1_12/tables_as_tabular.lua (branch v1.12-paper),
-- itself copied unchanged from papers/v0_42/. One change: a table of more than 32 body rows (the per-brand appendix,
-- up to 107 rows) is left to pandoc's longtable, which breaks across pages; every shorter table is rendered as below.
-- tables_as_tabular.lua -- pandoc filter for the v0.42 paper build (scripts/build_paper_v0_42.py).
-- Renders every table as an unbreakable booktabs tabular inside a table block placed here if it fits ([htbp]) with a numbered
-- caption, instead of pandoc's longtable. The v0.42 tables are short (at most 10 rows); longtable's page breaking
-- does not account for floats placed on the same page, which let figures run into the footer in the synthetic
-- pre-flight. Columns whose cells are long (over 45 characters) wrap in a p{} column; a table wider than the text
-- block is scaled down to the text width (graphicx \resizebox).

-- Fixed column widths (fractions of the line width; nil = natural width) for tables named by the start of their
-- caption. Table 1 (the pre-registered hypotheses) was scaled down to fit the text block, which made its type
-- smaller than the other tables; with wrapped columns it fits at the tables' normal size.
local FIXED = {
  ["Pre-registered hypotheses, quoted"] = {nil, nil, 0.33, 0.19, 0.17},
}

local function render(blocks)
  local s = pandoc.write(pandoc.Pandoc(blocks), 'latex')
  return (s:gsub('%s*\n%s*', ' '))
end

local function cell_text(c)
  return pandoc.utils.stringify(c.contents)
end

local function row(r)
  local cells = {}
  for _, c in ipairs(r.cells) do
    table.insert(cells, render(c.contents))
  end
  return table.concat(cells, ' & ') .. ' \\\\'
end

function Table(tbl)
  local nrows = 0
  for _, b in ipairs(tbl.bodies) do nrows = nrows + #b.body end
  if nrows > 32 then return nil end
  local ncol = #tbl.colspecs
  local maxlen = {}
  for i = 1, ncol do maxlen[i] = 0 end
  local function scan(r)
    for i, c in ipairs(r.cells) do
      local n = utf8.len(cell_text(c)) or #cell_text(c)
      if n > maxlen[i] then maxlen[i] = n end
    end
  end
  for _, b in ipairs(tbl.bodies) do for _, r in ipairs(b.body) do scan(r) end end
  local nlong = 0
  for i = 1, ncol do if maxlen[i] > 45 then nlong = nlong + 1 end end
  local fixed = nil
  local captext = pandoc.utils.stringify(tbl.caption.long)
  for k, w in pairs(FIXED) do
    if captext:sub(1, #k) == k then fixed = w end
  end
  local spec = {}
  for i, cs in ipairs(tbl.colspecs) do
    local a = tostring(cs[1])
    if fixed and fixed[i] then
      spec[i] = string.format('>{\\raggedright\\arraybackslash}p{%.2f\\linewidth}', fixed[i])
    elseif fixed then spec[i] = 'l'
    elseif maxlen[i] > 45 then
      spec[i] = string.format('>{\\raggedright\\arraybackslash}p{%.2f\\linewidth}', 0.62 / nlong)
    elseif a == 'AlignRight' then spec[i] = 'r'
    elseif a == 'AlignCenter' then spec[i] = 'c'
    else spec[i] = 'l' end
  end
  local out = {'\\begin{table}[htbp]', '\\centering', '\\small'}
  local cap = render(tbl.caption.long)
  if cap ~= '' then table.insert(out, '\\caption{' .. cap .. '}') end
  table.insert(out, '\\resizebox{\\ifdim\\width>\\linewidth\\linewidth\\else\\width\\fi}{!}{%')
  table.insert(out, '\\begin{tabular}{' .. table.concat(spec) .. '}')
  table.insert(out, '\\toprule')
  for _, r in ipairs(tbl.head.rows) do table.insert(out, row(r)) end
  table.insert(out, '\\midrule')
  for _, b in ipairs(tbl.bodies) do
    for _, r in ipairs(b.body) do table.insert(out, row(r)) end
  end
  table.insert(out, '\\bottomrule')
  table.insert(out, '\\end{tabular}')
  table.insert(out, '}')
  table.insert(out, '\\end{table}')
  return pandoc.RawBlock('latex', table.concat(out, '\n'))
end
