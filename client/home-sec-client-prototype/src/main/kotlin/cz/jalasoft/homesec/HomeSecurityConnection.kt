package cz.jalasoft.homesec

import java.net.Proxy
import java.net.URL
import java.net.URLConnection
import java.security.KeyStore
import javax.net.ssl.*


internal class HomeSecurityConnection {

    companion object {

        fun connect(url : String, proxy : Proxy?) : HttpsURLConnection {

            val connection : URLConnection = if (proxy == null) {
                URL(url).openConnection()
            } else {
                URL(url).openConnection(proxy)
            }

            if (connection is HttpsURLConnection) {
                connection.sslSocketFactory = sslSocketFactory()
                return connection
            }

            throw IllegalStateException("Https connection expected.")
        }

        private fun sslSocketFactory() : SSLSocketFactory {

            val context = SSLContext.getInstance("SSL")

            context.init(keyManager(), trustManager(), null)

            return context.socketFactory
        }

        private fun keyManager() : Array<KeyManager> {
            val factory = KeyManagerFactory.getInstance(KeyManagerFactory.getDefaultAlgorithm())
            val keyStore = KeyStore.getInstance("JKS")

            javaClass.classLoader.getResourceAsStream("client_keystore.jks").use {
                keyStore.load(it, "hovnicko".toCharArray())
            }

            factory.init(keyStore, "hovnicko".toCharArray())
            return factory.keyManagers
        }

        private fun trustManager() : Array<TrustManager> {
            val factory = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm())

            javaClass.classLoader.getResourceAsStream("store.jks").use {
                val store = KeyStore.getInstance("JKS")
                store.load(it, "hovnicko".toCharArray())
                factory.init(store)
                return factory.trustManagers
            }
        }
    }
}