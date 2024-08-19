package main

import (
	"io/ioutil"
	"log"
	"os/exec"
	"path/filepath"
	"regexp"
	"sort"
	"strconv"
	"sync"
)

func extractNumericPart(filename string) int {
	re := regexp.MustCompile(`\d+`)
	match := re.FindString(filename)
	if match == "" {
		return int(^uint(0) >> 1) // Max int value
	}
	num, _ := strconv.Atoi(match)
	return num
}

func processFile(filePath string, wg *sync.WaitGroup) {
	defer wg.Done()
	cmd := exec.Command("ascii-image-converter.exe", filePath)
	err := cmd.Run()
	if err != nil {
		log.Printf("Failed to process file %s: %v", filePath, err)
	}
}

func openFilesInOrder(directory string) {
	files, err := ioutil.ReadDir(directory)
	if err != nil {
		log.Fatalf("Failed to read directory: %v", err)
	}

	var pngFiles []string
	for _, file := range files {
		if filepath.Ext(file.Name()) == ".png" {
			pngFiles = append(pngFiles, file.Name())
		}
	}

	sort.Slice(pngFiles, func(i, j int) bool {
		return extractNumericPart(pngFiles[i]) < extractNumericPart(pngFiles[j])
	})

	var wg sync.WaitGroup
	for _, file := range pngFiles {
		wg.Add(1)
		go processFile(filepath.Join(directory, file), &wg)
		wg.Wait()
	}

	wg.Wait()
}

func main() {
	directoryPath := `C:\Users\Hp\Documents\workspace\BadApple\Frames-1`
	openFilesInOrder(directoryPath)
}
