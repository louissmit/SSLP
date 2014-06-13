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


function bleu.bleu(golds, outs)
    local gold_lengths = 0; local out_lengths = 0
	local ps = {0, 0, 0, 0}
    for i, gold in pairs(golds) do
        local out = outs[i]
        gold_lengths = gold_lengths + #gold
        out_lengths = out_lengths + #out
        -- unigram
        ps[1] = ps[1] + precision(gold, out)
        for n = 2, 4 do
            local gold_ngram = ngrams(gold, n)
            local out_ngram = ngrams(out, n)
            local ps_sample = precision(gold_ngram, out_ngram)

            ps[n] = ps[n] + ps_sample
        end
--        print(ps)
    end
    local bp = math.min(1, math.exp(1 - (gold_lengths/ out_lengths)))

    local res = bp
    for i= 1,4 do
        res = res * (ps[i] / #golds)
--        print(ps[i] / #golds)
--        res = res + math.log(ps[i]) - math.log(#golds)
    end
    return res^(1/4)
--    print(math.exp(res)^(1/4))
end

function test_bleu()
    local f = assert(io.open('../data/100000/train.de', "r"))
    local f_gprimes = assert(io.open('../data/100000/train.de.prime', "r"))
    local i = 0
    local n = 99415
    local golds = {} ; local outs = {}
    while i < n do
        local out = split(f:read())
        local gold = split(f_gprimes:read())
        table.insert(golds, gold)
        table.insert(outs, out)
        i = i + 1
    end
    bleu.bleu(golds, outs)

end

--test_bleu()
return bleu