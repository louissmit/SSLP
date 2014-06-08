--
-- Created by IntelliJ IDEA.
-- User: louissmit
-- Date: 6/8/14
-- Time: 8:55 PM
-- To change this template use File | Settings | File Templates.
--

bleu = {}

local function ngrams(s, n)
    local result = ""
    for i = 1, #s - n +1 do
        for j = i, i+n  do
            result = result.." "..s[j]
--            table.insert(result, s[j])
        end
    end
	return result
end

local function precision(gold, out)
	if gold == nil or out == nil then
		return 1
    end
    local right = 0
    local count = 0
    local done = {}
    for _, g in pairs(gold) do
        for _, o in pairs(out) do
            if not done[o] then
                done[o] = true
                count = count + 1
                if g == o then
                    right = right + 1
                end
            end

        end
    end
    return right / count

--	return len(set(gold) & set(out)) / len(set(out))
end



function bleu.bleu(gold, out)
	local bp = min(1, len(out) / len(gold))
	local ps = {}
	for n = 1, 4 do
        table.insert(ps, precision(ngrams(gold, n), ngrams(out, n)))
    end

	return bp * ps[1] * ps[2] * ps[3] * ps[4]
end


return bleu