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
require('BLEUCriterion')

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

function train_nn(g_primes, word_vecs, input_size, hu_sizes, epochs, learning_rate)
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

    local count = 0
    local function add_to_batch(batch, vector, label)
        count = count + 1
--        print('adding sample '..tostring(count))
        table.insert(batch, {vector, label})
    end
    local batch_size = 100
    local batch = {}
    local sample_size = 10
    local sampled = {}
    for _, g_prime in pairs(g_primes) do
        local sample_count = 0
        if #g_prime ~= 1 then
            while sample_count < sample_size do
                local i = math.ceil(torch.rand(1)[1]*#g_prime)
                local j = math.ceil(torch.rand(1)[1]*#g_prime)
                if i~=j and not sampled[{i,j}] then
                    local true_vector = features(word_vecs, g_prime, i, j)
                    criterion:forward(mlp:forward(true_vector), 1)
                    add_to_batch(batch, true_vector, 1)

                    local false_vector = features(word_vecs, g_prime, i, j, true)
                    add_to_batch(batch, false_vector, -1)
                    sampled[{i,j}] = true
                    sample_count = sample_count + 1
                end
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
    word_vecs:load(361068)
--    local f = assert(io.open('../../project2_data/training/p2_training.nl', "r"))
    local train_primes = assert(io.open('../data/100000/train.de.prime', "r"))
--    local test = assert(io.open('../data/100000/test.de', "r"))

    local train_set = {}
    local n = 0
    local train_size = 1000
    local test_size = 100
    local sent_size = 10
    while n < train_size do
        local t = train_primes:read()
        local sent = split(t)
        if #sent < sent_size then
            table.insert(train_set, sent)
            n = n + 1
        end
    end
    print(train_set)

    local mlp = train_nn(train_set, word_vecs, 2100, {256, 64}, 10, 0.01)
    local test_set = {}
    while (n - train_size) < test_size do
        local t = train_primes:read()
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

gut, total, mlp = main()
--word_vecs = WordVecs:new()
--word_vecs:load_from_word2vec('../data/word_vecs_europarl')
--word_vecs:save()
