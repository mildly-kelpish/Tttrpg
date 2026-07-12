#include <cstdio>
#include <iostream>
#include "libraries/rang.hpp"
#include "libraries/toml.hpp"
#include "libraries/httplib.h"
#include "libraries/json.hpp"

using namespace std;
using namespace rang;
using json = nlohmann::json;


int main() {
    cout << rang::fg::cyan << "HTTRPG official client v1.0" << rang::style::reset << std::endl;
    const toml::value config = toml::parse("config.toml");
    cout << "loaded config" << std::endl;
    httplib::Client cli(config.at("SERVER").as_string());
    cout << "connecting to server..." << std::endl; // why printf when cout << "string" << std::endl; 
    nlohmann::json authentication = {{"key", config.at("PLAYERKEY").as_string()}, {"typ", config.at("PLAYERTYPE").as_integer()}};
    cout << authentication.dump() << std::endl;
    auto res = cli.Post("/authenticate", authentication.dump(), "application/json");
    if (res) {
        cout << "loading complete!" << std::endl;
        cout << res->body << std::endl;
    }
    


    return 0;
}