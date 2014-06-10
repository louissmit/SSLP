--
-- Created by IntelliJ IDEA.
-- User: louissmit
-- Date: 6/7/14
-- Time: 2:14 PM
-- To change this template use File | Settings | File Templates.
--
WordVecs = require('word_vecs')
require('nn')
split = require('utils').split
bleu = require('bleu').bleu

function features(word_vecs, sent, left, right, flip, vector_size)
    if flip == nil then flip = false end
    if vector_size == nil then vector_size = 300 end

    local function get(i)
   		if i > 0 and i < #sent then
			return word_vecs:get(sent[i])
		else
			return torch.Tensor(vector_size)
        end
    end
    local sum = torch.Tensor(vector_size)
    for i = left+1, right-1 do
        sum:add(get(i))
    end
    if flip then
        left, right = right, left
    end
    local res = get(left-1)
    for _, i in pairs({left, left+1}) do
        res = torch.cat(res, get(i), 1)
    end
    res = torch.cat(res, sum, 1)
    for _, i in pairs({right-1, right, right+1}) do
        res = torch.cat(res, get(i), 1)
    end
    return res

end

function train_nn(input_size, hu_size, g_primes, word_vecs)
    local timer = torch.Timer()
    local mlp = nn.Sequential();  -- make a multi-layer perceptron
    local output_size = 1
    local learning_rate = 0.01

    mlp:add(nn.Linear(input_size, hu_size))
    mlp:add(nn.Tanh())
--    mlp:add(nn.Linear(hu_size, hu_size))
--    mlp:add(nn.Tanh())
    mlp:add(nn.Linear(hu_size, output_size))

    local criterion = nn.MarginCriterion()
    local trainer = nn.StochasticGradient(mlp, criterion)
    trainer.maxIteration = 2
    trainer.learningRate = learning_rate

    local function add_to_batch(batch, vector, label)
        table.insert(batch, {vector, label})
    end
    local batch_size = 100
    local batch = {}
    local count = 1
    for _, g_prime in pairs(g_primes) do
        for i = 1, #g_prime do
            for j = i+1, #g_prime do
--                if count % batch_size == 0 then
--                    function batch:size() return batch_size end
--                    print(batch:size())
--                    trainer:train(batch)
--                    batch = {}
--                end

                local true_vector = features(word_vecs, g_prime, i, j)
                add_to_batch(batch, true_vector, 1)

                local false_vector = features(word_vecs, g_prime, i, j, true)
                add_to_batch(batch, false_vector, -1)
                count = count + 1
            end
        end
    end

    function batch:size() return #batch end
    print(batch:size())
    trainer:train(batch)
    print(timer:time().real)
    return mlp
end

function test_sample(word_vecs, g_primes, mlp)
   local total = 0
   local gut = 0
   for _, g_prime in pairs(g_primes) do
       print(g_prime)
        for i = 1, #g_prime do
            for j = i+1, #g_prime do
                local true_vector = features(word_vecs, g_prime, i, j)
                local res = mlp:forward(true_vector)
                if res[1] > 0 then
                    gut = gut + 1
                end
                total = total + 1
                local false_vector = features(word_vecs, g_prime, i, j, true)
                local res = mlp:forward(false_vector)
                if res[1] < 0 then
                    gut = gut + 1
                end
                total = total + 1
            end
        end
   end
   return gut, total
end

function main()
    local word_vecs = WordVecs:new()
    word_vecs:load(100000)
    local f = assert(io.open('../../project2_data/training/p2_training.nl', "r"))
    local f_gprimes = assert(io.open('../gprimes_n=10000', "r"))

    local train_set = {}
    local n = 0
    local train_size = 50
    local test_size = 20
    local sent_size = 10
    while n < train_size do
        local t = f:read()
        local sent = split(t)
        if #sent < sent_size then
            table.insert(train_set, sent)
            n = n + 1
        end
    end
    print(train_set)

    local mlp = train_nn(2100, 500, train_set, word_vecs)
    local test_set = {}
    while (n - train_size) < test_size do
        local t = f:read()
        local sent = split(t)
        if #sent < sent_size then
            table.insert(test_set, sent)
            n = n + 1
        end
    end

    local gut, total = test_sample(word_vecs, test_set, mlp)
    print(gut/total)
    return gut, total, mlp
end

function test_bleu()
    local f = assert(io.open('../data/100000/train.de', "r"))
    local f_gprimes = assert(io.open('../data/100000/train.de.prime', "r"))
    local i = 0
    local n = 99415
    local res = 0
    while i < n do
        local nl = split(f:read())
        local prime = split(f_gprimes:read())
        res = res + bleu(prime, nl)
        i = i + 1
    end
    print(res / n)

end
test_bleu()
--gut, total, mlp = main()
--word_vecs = WordVecs:new()
--word_vecs:load_from_word2vec(100000)
--word_vecs:save()
