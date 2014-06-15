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
B = require("B")
require('localsearch')
features = require('utils').features
--require('BLEUCriterion')



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
    print('batch size:', batch:size())
    trainer:train(batch)
    print('training time:', timer:time().real)
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

function test_network(word_vecs, train_size, test_size, sample_size, hidden_units, learning_rate, prediction_test, mlp)
    local test = assert(io.open('../data/100000/test.de', "r"))
    local test_primes = assert(io.open('../data/100000/test.de.prime', "r"))
	local mlp
    if mlp == nil then
        mlp = torch.load('MLP:n='..tostring(train_size)..'_sample_size='..tostring(sample_size)..'_epochs=10'..'_hidden_units='
                ..tostring(hidden_units[1])..','..tostring(hidden_units[2])..'_learning_rate'..tostring(learning_rate))
    end
    -- create test set
    local test_set = {}
    local test_set_prime = {}
    local n = 0
    while n < test_size do
        local t = test:read()
        local t_prime = test_primes:read()
        local sent = split(t)
        local sent_prime = split(t_prime)
         if #sent < 10 then
            table.insert(test_set, sent)
            table.insert(test_set_prime, sent_prime)
            n = n + 1
         end
    end
    if prediction_test then
        local gut, total = test_sample(word_vecs, test_set_prime, mlp, sample_size)
        print('prediction test: ', gut/total)
    end

    print('BLEU:', bleu(test_set_prime, test_set))
    local b = B:new(mlp, word_vecs)

    local old_bleu_score = 0
    local bleu_score = 0.1
    local improved_rounds = 0
    while improved_rounds < 10 do
        old_bleu_score = bleu_score
        local permuted_test_set = run_on_corpus(test_set, b)
        bleu_score = bleu(test_set_prime, permuted_test_set)
        test_set = permuted_test_set
        print('BLEU permuted:', bleu_score)
        if(old_bleu_score - bleu_score) > 0 then improved_rounds = improved_rounds + 1 end
    end


    return mlp, permuted_test_set
end

function main(retrain)
    local word_vecs = WordVecs:new()
    word_vecs:load(100000)
--    local f = assert(io.open('../../project2_data/training/p2_training.nl', "r"))
    local train_primes = assert(io.open('../data/100000/train.de.prime', "r"))

    local train_size = 90000
    local test_size = 100
    local sample_size = 10
    local learning_rate = 0.01
    local epochs = 10
    local hidden_units = {512, 128}
    local input_size = 2100

    if retrain then
        local train_set = {}
        local n = 0
        -- create train set
        while n < train_size do
            local t = train_primes:read()
            local sent = split(t)
            table.insert(train_set, sent)
            n = n + 1
        end

        -- train MLP
        local mlp = train_nn(train_set, word_vecs, input_size, hidden_units, epochs, learning_rate, sample_size)
        torch.save('MLP:n='..tostring(train_size)..'_sample_size='..tostring(sample_size)..'_epochs=10'..'_hidden_units='
                ..tostring(hidden_units[1])..','..tostring(hidden_units[2])..'_learning_rate'..tostring(learning_rate), mlp)

    end

    local mlp, permuted_test_set = test_network(word_vecs, train_size, test_size, sample_size, hidden_units, learning_rate, true, mlp)

    return mlp, permuted_test_set
end

mlp, permuted_test_set = main(false)
--word_vecs = WordVecs:new(100000)
--word_vecs:load_from_word2vec('../data/word_vecs_europarl')
--word_vecs:save()
