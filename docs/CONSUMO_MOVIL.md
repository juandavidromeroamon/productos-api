# Consumo de la API desde una app móvil

La API ya trae CORS abierto y devuelve JSON plano, así que cualquier cliente HTTP la consume sin
configuración extra. Estos ejemplos cubren los dos escenarios más probables.

## URLs según el entorno

| Entorno | Base URL |
|---------|----------|
| Emulador Android | `http://10.0.2.2:8000` |
| Simulador iOS | `http://127.0.0.1:8000` |
| Celular físico en la misma WiFi | `http://IP_DE_TU_PC:8000` |
| Producción | `https://TU-SERVICIO.onrender.com` |

Para probar contra un backend local en HTTP desde Android hay que habilitar tráfico en claro en
el `AndroidManifest.xml`:

```xml
<application android:usesCleartextTraffic="true" ... >
```

Con la URL de producción en HTTPS esto no hace falta.

---

## Kotlin + Retrofit

```kotlin
data class ProductoResponse(
    val id: Int,
    val nombre: String,
    val precio: Double,
    val stock: Int,
    val categoria: String,
    val valor_en_inventario: Double
)

data class ListaProductosResponse(
    val criterio: String,
    val total: Int,
    val productos: List<ProductoResponse>
)

data class ValorInventarioResponse(
    val valor_total: Double,
    val cantidad_productos: Int,
    val unidades_totales: Int,
    val moneda: String
)

interface ProductosApi {

    @GET("api/v1/productos")
    suspend fun listar(): List<ProductoResponse>

    @GET("api/v1/productos/precio-mayor")
    suspend fun precioMayor(@Query("valor") valor: Double = 100000.0): ListaProductosResponse

    @GET("api/v1/productos/mayor-stock")
    suspend fun mayorStock(): ProductoResponse

    @GET("api/v1/productos/categoria/{categoria}")
    suspend fun porCategoria(@Path("categoria") categoria: String): ListaProductosResponse

    @GET("api/v1/productos/{id}")
    suspend fun porId(@Path("id") id: Int): ProductoResponse

    @GET("api/v1/productos/conteo-por-categoria")
    suspend fun conteoPorCategoria(): ConteoResponse

    @GET("api/v1/inventario/valor-total")
    suspend fun valorInventario(): ValorInventarioResponse
}

object ApiClient {
    private const val BASE_URL = "https://TU-SERVICIO.onrender.com/"

    val api: ProductosApi by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ProductosApi::class.java)
    }
}
```

Dependencias en `build.gradle.kts`:

```kotlin
implementation("com.squareup.retrofit2:retrofit:2.11.0")
implementation("com.squareup.retrofit2:converter-gson:2.11.0")
```

Y el permiso de internet en el manifiesto:

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

---

## .NET MAUI + HttpClient

```csharp
public record ProductoResponse(
    int Id,
    string Nombre,
    double Precio,
    int Stock,
    string Categoria,
    double Valor_En_Inventario);

public class ProductosApiService
{
    private readonly HttpClient _http;
    private static readonly JsonSerializerOptions Opciones =
        new() { PropertyNameCaseInsensitive = true };

    public ProductosApiService(HttpClient http)
    {
        _http = http;
        _http.BaseAddress = new Uri("https://TU-SERVICIO.onrender.com/");
    }

    public async Task<List<ProductoResponse>> ListarAsync()
    {
        var json = await _http.GetStringAsync("api/v1/productos");
        return JsonSerializer.Deserialize<List<ProductoResponse>>(json, Opciones) ?? new();
    }

    public async Task<ProductoResponse?> ObtenerPorIdAsync(int id)
    {
        var respuesta = await _http.GetAsync($"api/v1/productos/{id}");
        if (respuesta.StatusCode == HttpStatusCode.NotFound)
            return null;

        respuesta.EnsureSuccessStatusCode();
        var json = await respuesta.Content.ReadAsStringAsync();
        return JsonSerializer.Deserialize<ProductoResponse>(json, Opciones);
    }
}
```

---

## Pantallas sugeridas para la app de evidencia

Una app de tres pantallas alcanza para demostrar el consumo completo:

1. **Listado** — consume `GET /api/v1/productos` y muestra nombre, precio y stock en un RecyclerView o CollectionView.
2. **Detalle** — al tocar un item, consume `GET /api/v1/productos/{id}`.
3. **Resumen** — consume `GET /api/v1/inventario/valor-total` y `GET /api/v1/productos/conteo-por-categoria`, con un filtro por categoría que llame a `GET /api/v1/productos/categoria/{categoria}`.

Con eso quedan cubiertas las seis operaciones del enunciado desde la interfaz móvil.
