/* -----------------------------------------------------------
Course: CSE 251
Lesson Week: 12
File: team1.go
Purpose: Process URLs
Instructions:
Part 1
- Take this program and use goroutines for the function getPerson().
Part 2
- Create a function "getSpecies()" that will receive the following urls
  using that function as a goroutine.
- For a species, display name, average_height and language

----------------------------------------------------------- */
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"sync"
	"time"
)

type Species struct {
	Name             string
	Classification   string
	Designation      string
	Average_height   string
	Skin_colors      string
	Hair_colors      string
	Eye_colors       string
	Average_lifespan string
	Homeworld        string
	Language         string
	People           []string
	Films            []string
	Created          time.Time
	Edited           time.Time
	Url              string
}

func getSpecies(url string) {
	// make a sample HTTP GET request
	res, err := http.Get(url)

	// check for response error
	if err != nil {
		log.Fatal(err)
	}

	// read all response body
	data, _ := ioutil.ReadAll(res.Body)

	// close response body
	res.Body.Close()

	//fmt.Println("data=", string(data))

	species := Species{}

	jsonErr := json.Unmarshal(data, &species)
	if jsonErr != nil {
		log.Fatal(jsonErr)
		fmt.Println("ERROR Pasing the JSON")
	}

	fmt.Println("-----------------------------------------------")
	//fmt.Println(species)
	fmt.Println("Name: ", species.Name)
	fmt.Println("Average Height: ", species.Average_height)
	fmt.Println("Language: ", species.Language)
}

func agahr() {

	var wg sync.WaitGroup

	urls := []string{
		"http://swapi.dev/api/species/1/",
		"http://swapi.dev/api/species/2/",
		"http://swapi.dev/api/species/3/",
		"http://swapi.dev/api/species/6/",
		"http://swapi.dev/api/species/15/",
		"http://swapi.dev/api/species/19/",
		"http://swapi.dev/api/species/20/",
		"http://swapi.dev/api/species/23/",
		"http://swapi.dev/api/species/24/",
		"http://swapi.dev/api/species/25/",
		"http://swapi.dev/api/species/26/",
		"http://swapi.dev/api/species/27/",
		"http://swapi.dev/api/species/28/",
		"http://swapi.dev/api/species/29/",
		"http://swapi.dev/api/species/30/",
		"http://swapi.dev/api/species/33/",
		"http://swapi.dev/api/species/34/",
		"http://swapi.dev/api/species/35/",
		"http://swapi.dev/api/species/36/",
		"http://swapi.dev/api/species/37/",
	}

	for _, url := range urls {
		uurl := url
		wg.Add(1)
		go func() {
			defer wg.Done()
			getSpecies(uurl)
		}()
	}

	wg.Wait()

	fmt.Println("All done!")
}
