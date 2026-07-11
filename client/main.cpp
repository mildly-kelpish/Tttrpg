#include <cstdio>
#include <iostream>
#include "libraries/rang.hpp"
#include "libraries/toml.hpp"
#include "libraries/httplib.h"
#include "libraries/json.hpp"

using namespace std;
using namespace rang;


int main() {
    cout << rang::fg::cyan << "HTTRPG official client v1.0" << rang::style::reset << std::endl;
    toml::table config;
    std::optional<std::string> serveradress;
    std::optional<std::string> playerkey;
    std::optional<std::long> playertype;
    try {
        config = toml::parse_file("config.toml");
        serveradress = config["SERVER"].value<std::string>();
        playerkey = config["PLAYERKEY"].value<std::string>();
        playertype = config["PLAYERTYPE"].value<std::long>();
        cout << rang::fg::yellow << "loaded configuration file" << rang::style::reset << std::endl;
    }
    catch (const toml::parse_error& err) {
        cerr << rang::fg::red << "ERROR: parsing failed!:\n" << err << "\n" << rang::style::reset << std::endl;
        return 1;
    }
    httplib::Client cli(*serveradress);
    cout << "connecting to server..." << std::endl; // why printf when cout << "string" << std::endl; !
    nlohman::json authentication == {{"typ"}}
    auto res = cli.Post("/authenticate", );
    if (res && res-> status == 200) {
        cout << "loading complete!" << std::endl;
        cout << res->body << std::endl;
    }
    


    return 0;
}
