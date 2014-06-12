--
-- Created by IntelliJ IDEA.
-- User: louissmit
-- Date: 6/8/14
-- Time: 8:55 PM
-- To change this template use File | Settings | File Templates.
--

split = require('utils').split
bleu = {}

local function ngrams(s, n)
    local result = {}
    for i = 1, #s - n + 1 do
        local ngram = table.concat({unpack(s, i, i+n-1)}, " ")
        table.insert(result, ngram)
    end
	return result
end

local function precision(gold, out)
	if #gold == 0 or #out == 0 then
		return 1
    end
    local right = 0
    local count = 0
    local done = {}
    for _, o in pairs(out) do
        if done[o] == nil then
            count = count + 1
            done[o] = true
            for _, g in pairs(gold) do
                if g == o then
                    right = right + 1
                    break
                end
            end
        end

    end

    return right /count
end


function bleu.bleu(gold, out)
--	local bp = math.min(1, math.exp(1 - (#gold/ #out)))
    local bp = 1
	local ps = {}
    -- unigram
    table.insert(ps, precision(gold, out))
	for n = 2, 4 do
        local gold_ngram = ngrams(gold, n)
        local out_ngram = ngrams(out, n)
        local ps_sample = precision(gold_ngram, out_ngram)

        table.insert(ps, ps_sample)
    end
	return bp * (ps[1] * ps[2] * ps[3] * ps[4])^(1/4), ps
end

function test_bleu()
    local f = assert(io.open('../data/100000/train.de', "r"))
    local f_gprimes = assert(io.open('../data/100000/train.de.prime', "r"))
    local i = 0
    local n = 99415
    local res = 0
    local ps_tot = {0, 0, 0, 0}
    while i < n do
        local nl = split(f:read())
        local prime = split(f_gprimes:read())
        x, ps = bleu(prime, nl)
        for i= 1,4 do
            ps_tot[i] = ps_tot[i] + ps[i]
        end
        res = res + x
        i = i + 1
    end
    for i= 1,4 do
        print(ps_tot[i] / n)
    end
    print((res / n))

end

return bleu