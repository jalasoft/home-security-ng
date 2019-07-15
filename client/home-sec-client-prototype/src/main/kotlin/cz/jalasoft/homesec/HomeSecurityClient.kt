package cz.jalasoft.homesec

import com.fasterxml.jackson.annotation.JsonCreator
import com.fasterxml.jackson.annotation.JsonProperty
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import java.net.InetSocketAddress
import java.net.Proxy


class HomeSecurityClient(private val ip : String, private val proxy : Proxy?) {

    private val mapper = jacksonObjectMapper()

    constructor(ip: String) : this(ip, null)

    constructor(ip: String, ipAddr : String, ipPort : Int) : this(ip, Proxy(Proxy.Type.HTTP, InetSocketAddress(ipAddr, ipPort)))

    fun getFrame(name: String, quality : FrameQuality) : Frame {
        val url = "https://${ip}:443/api/camera/${name}?quality=${quality.code}"
        return invoke(url, Frame::class.java)
    }

    fun getFrame(name: String, resolution : Resolution) : Frame {
        return getFrame(name, resolution.id)
    }

    fun getFrame(name: String, qualityId : Int) : Frame {
        val url = "https://${ip}:443/api/camera/${name}?quality=${qualityId}"
        return invoke(url, Frame::class.java)
    }

    fun getSupportedResolutions(name: String) : SupportedResolutions {
        val url = "https://${ip}:443/api/camera/${name}/resolution"
        val list : Array<Resolution> = invoke(url, Array<Resolution>::class.java)
        return SupportedResolutions(list)
    }

    private fun <T> invoke(url : String, type : Class<T>) : T {
        return HomeSecurityConnection.connect(url, proxy).let {
            it.connect()

            if (it.responseCode != 200) {
                throw HomeSecurityException(it.responseMessage)
            }

            it.inputStream.use {

                return mapper.readValue(it, type)
            }
        }
    }
}

class Frame {

    val data : String
    val width : Int
    val height: Int

    @JsonCreator
    constructor(
            @JsonProperty("data")
            data : String,
            @JsonProperty("resolution_width")
            width : Int,
            @JsonProperty("resolution_height")
            height: Int
            ) {

        this.data = data
        this.width = width
        this.height = height
    }

    override fun toString(): String {
        return "Frame[${width}X${height}:${data}]"
    }
}

data class Resolution(val id : Int, val width : Int, val height : Int)

class SupportedResolutions(private val resolutions : Array<Resolution>) {

    fun best(): Resolution {
        return resolutions.first();
    }

    fun medium() : Resolution {
        return resolutions[resolutions.size / 2]
    }

    fun worst() : Resolution {
        return resolutions.last()
    }

    fun size() : Int {
        return resolutions.size
    }

    operator fun get(i : Int) : Resolution {
        return resolutions[i]
    }

    fun forEach(block : (Resolution) -> Unit) {
        resolutions.forEach(block)
    }
}

enum class FrameQuality(val code : String) {
    WORST("worst"), MEDIUM("medium"), BEST("best")
}