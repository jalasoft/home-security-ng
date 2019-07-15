package cz.jalasoft.homesec

import java.nio.file.Files
import java.nio.file.Paths
import java.util.*


object FileSaver {

    fun save(path : String, data : String) {

        val decoder = Base64.getDecoder()
        val decoded_data = decoder.decode(data)

        val file = Paths.get(path)

        Files.write(file, decoded_data)
    }
}