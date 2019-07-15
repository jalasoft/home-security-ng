package cz.jalasoft.homesec


fun main() {

    val client = HomeSecurityClient("77.104.252.65", "proxy.private.fio.cz", 8080)


    val res = client.getSupportedResolutions("obyvak1")

    /*
    for (i in 0 until res.size()) {
        val resolution = res[i]

        println(resolution)
    }*/

    res.forEach { println(it) }

    res.best().also { println("best: ${it}") }
    res.medium().also { println("medium: ${it}") }
    res.worst().also { println("worst: ${it}") }

    client.getFrame("obyvak1", res.medium())
            .also {
                println("resolution: ${it.width}X${it.height}")
            }.also {
                FileSaver.save("/home/FIO_DOM/lastovicka/obrazek17.jpg", it.data)
            }

/*
    for(i in 0 until res.size()) {

        client.getFrame("obyvak", res[i]).also {
            println("resolution: ${it.width}X${it.height}")
            FileSaver.save("/home/FIO_DOM/lastovicka/obrazek${i}.jpg", it.data)
        }

        Thread.sleep(3000)
    }*/
}