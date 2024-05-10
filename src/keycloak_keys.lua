local url = require "socket.url"
local http = require("resty.http")
local cjson_safe = require "cjson.safe"
local convert = require "kong.plugins.jwt-keycloak.key_conversion"

local function get_request(url)
    -- Can't instanciate this in the module scope because the `require` can't be done at any time:
    -- https://github.com/Kong/kong/issues/3271
    local httpc = http.new()

    local res, err = httpc:request_uri(url, {
        method = "GET",
    })

    if err then
        return nil, 'Error while calling url ' .. url .. ': ' .. err
    end

    if res.status ~= 200 then
        return nil, 'Failed calling url ' .. url .. ' response status ' .. res.status
    end

    res, err = cjson_safe.decode(res.body)
    if not res then
        return nil, 'Failed to parse json response'
    end

    return res, nil
end

local function get_wellknown_endpoint(well_known_template, issuer)
    return string.format(well_known_template, issuer)
end

local function get_issuer_keys(well_known_endpoint)
    local res, err = get_request(well_known_endpoint)
    if err then
        return nil, err
    end

    local res, err = get_request(res['jwks_uri'])
    if err then
        return nil, err
    end

    local keys = {}
    for i, key in ipairs(res['keys']) do
        keys[i] = string.gsub(
            convert.convert_kc_key(key), 
            "[\r\n]+", ""
        )
    end
    return keys, nil
end

return {
    get_request = get_request,
    get_issuer_keys = get_issuer_keys,
    get_wellknown_endpoint = get_wellknown_endpoint,
}
