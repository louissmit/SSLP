--
-- Created by IntelliJ IDEA.
-- User: louissmit
-- Date: 6/7/14
-- Time: 5:48 PM
-- To change this template use File | Settings | File Templates.
--

utils = {}

function utils.split(string)
    local res = {}
    for i in string.gmatch(string, "%S+") do
        table.insert(res, i)
    end
    return res
end

function utils.factorial(n)
        if n == 0 then
        return 1
      else
        return n * factorial(n-1)
      end
end

return utils