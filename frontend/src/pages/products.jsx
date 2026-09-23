import axios from "axios"
import { useEffect, useState } from "react"

function Products() {
  const [products, setProducts] = useState([])

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axios.get("http://localhost:8000/products")

        console.log(response.data)

        setProducts(response.data)
      } catch (error) {
        console.error(error)
      }
    }

    fetchProducts()
  }, [])

  return (
    <div>
      <h1>Products</h1>

      {products.map((product) => (
        <div key={product.product_id}>
          <h2>{product.product_name}</h2>
          <p>{product.description}</p>
          <p>Price: ₹{product.price}</p>
        </div>
      ))}
    </div>
  )
}

export default Products