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
factorial = require('utils').factorial
bleu = require('bleu').bleu
--require('BLEUCriterion')

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

function sample_g_prime(word_vecs, batch, g_prime, sample_size)
    if #g_prime ~= 1 then
        local sample_count = 0
        local sampled = {}
        local max_samples = (factorial(#g_prime) / factorial(#g_prime - 2))
        if sample_size > max_samples then sample_size = max_samples end
        while sample_count < sample_size do
            local i = math.ceil(torch.rand(1)[1]*#g_prime)
            local j = math.ceil(torch.rand(1)[1]*#g_prime)
            local key = tostring(i)..tostring(j)

            if i~=j and not sampled[key] then

                local label
                local vector
                if i < j then
                    label = 1
                    vector = features(word_vecs, g_prime, i, j)
                else
                    label = -1
                    vector = features(word_vecs, g_prime, j, i, true)
                end
                table.insert(batch, {vector, label})
                sampled[key] = true

                sample_count = sample_count + 1
            end
        end
    end
end

function train_nn(g_primes, word_vecs, input_size, hu_sizes, epochs, learning_rate, sample_size)
    local timer = torch.Timer()
    local mlp = nn.Sequential();  -- make a multi-layer perceptron
    local output_size = 1

    mlp:add(nn.Linear(input_size, hu_sizes[1]))
    mlp:add(nn.Tanh())
    mlp:add(nn.Linear(hu_sizes[1], hu_sizes[2]))
    mlp:add(nn.Tanh())
    mlp:add(nn.Linear(hu_sizes[2], output_size))

    local criterion = nn.MarginCriterion()
    local trainer = nn.StochasticGradient(mlp, criterion)
    trainer.maxIteration = epochs
    trainer.learningRate = learning_rate

    local batch = {}
    for _, g_prime in pairs(g_primes) do
        sample_g_prime(word_vecs, batch, g_prime, sample_size)
    end

    function batch:size() return #batch end
    print(batch:size())
    trainer:train(batch)
    print(timer:time().real)
    return mlp
end

function test_sample(word_vecs, g_primes, mlp, sample_size)
   local total = 0
   local gut = 0
   local batch = {}

   for _, g_prime in pairs(g_primes) do
       sample_g_prime(word_vecs, batch, g_prime, sample_size)
   end
   for _, vl_pair in pairs(batch) do
       local vector = vl_pair[1]
       local label = vl_pair[2]
        local res = mlp:forward(vector)
        if (label == -1 and res[1] < 0) or (label == 1 and res[1] > 0) then
            gut = gut + 1
        end
       total = total + 1

   end

   return gut, total
end

function main()
    local word_vecs = WordVecs:new()
    word_vecs:load(100000)
--    local f = assert(io.open('../../project2_data/training/p2_training.nl', "r"))
    local train_primes = assert(io.open('../data/100000/train.de.prime', "r"))
--    local test = assert(io.open('../data/100000/test.de', "r"))

    local train_set = {}
    local n = 0
    local train_size = 1000
    local test_size = 100
    local sent_size = 100


    while n < train_size do
        local t = train_primes:read()
        local sent = split(t)
        if #sent < sent_size then
            table.insert(train_set, sent)
            n = n + 1
        end
    end
--    print(train_set)
    local sample_size = 10
    local learning_rate = 0.01
    local epochs = 10
    local hidden_units = {256, 64}
    local input_size = 2100

    local mlp = train_nn(train_set, word_vecs, input_size, hidden_units, epochs, learning_rate, sample_size)
    local test_set = {}
    while (n - train_size) < test_size do
        local t = train_primes:read()
        local sent = split(t)
        if #sent < sent_size then
            table.insert(test_set, sent)
            n = n + 1
        end
    end

    local gut, total = test_sample(word_vecs, test_set, mlp, sample_size)
    print(gut/total)
    return gut, total, mlp
end

gut, total, mlp = main()
--word_vecs = WordVecs:new(100000)
--word_vecs:load_from_word2vec('../data/word_vecs_europarl')
--word_vecs:save()
