--
-- Created by IntelliJ IDEA.
-- User: louissmit
-- Date: 6/8/14
-- Time: 8:55 PM
-- To change this template use File | Settings | File Templates.
--

bleu = {}

local function ngrams(s, n)
    local result = {}
    for i = 1, #s - n do
        local ngram = false
        for j = i, i+n  do
            if not ngram then
                ngram = s[j]
            else
                ngram = ngram.." "..s[j]
            end

        end
        table.insert(result, ngram)
    end
--    print(result)
	return result
end

local function precision(gold, out)
	if #gold == 0 or #out == 0 then
		return 1
    end
    local right = 0
    local count = 0
    local done = {}
    for _, g in pairs(gold) do
        for _, o in pairs(out) do
            if done[o] == nil then
                done[o] = true
                count = count + 1

            end
            if g == o then
                right = right + 1
            end

        end
    end
    return right / count

--	return len(set(gold) & set(out)) / len(set(out))
end



function bleu.bleu(gold, out)
	local bp = math.min(1, #out / #gold)
	local ps = {}
	for n = 1, 4 do
        table.insert(ps, precision(ngrams(gold, n), ngrams(out, n)))
    end
	return bp * ps[1] * ps[2] * ps[3] * ps[4]
end


return bleu