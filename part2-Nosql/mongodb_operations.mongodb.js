//Operation 1: Load Data (1 mark)
// Import the provided JSON file into collection 'products

//Operation 2: Basic Query (2 marks)
// Find all products in "Electronics" category with price less than 50000
// Return only: name, price, stock
use('fleximart');
db.products.find(
  {
    category: "Electronics",
    price: { $lt: 50000 }
  },
  { 
    name: 1,
    price: 1,
    stock: 1,
    _id: 0
  }
)
// Output :
// [
//   {
//     "name": "Sony WH-1000XM5 Headphones",
//     "price": 29990,
//     "stock": 200
//   },
//   {
//     "name": "Dell 27-inch 4K Monitor",
//     "price": 32999,
//     "stock": 60
//   },
//   {
//     "name": "OnePlus Nord CE 3",
//     "price": 26999,
//     "stock": 180
//   }
// ]

//Operation 3: Review Analysis (2 marks)
// Find all products that have average rating >= 4.0
// Use aggregation to calculate average from reviews array

db.products.aggregate([
  {
    $addFields: {
      avgRating: { $avg: "$reviews.rating" }
    }
  },
  {
    $match: {
      avgRating: { $gte: 4.0 }
    }
  },
  {
    $project: {
      name: 1,
      avgRating: 1,
      _id: 0
    }
  }
])
// Output :
// [
//   {
//     "name": "Samsung Galaxy S21 Ultra",
//     "avgRating": 4.666666666666667
//   },
//   {
//     "name": "Apple MacBook Pro 14-inch",
//     "avgRating": 5
//   },
//   {
//     "name": "Sony WH-1000XM5 Headphones",
//     "avgRating": 4.666666666666667
//   },
//   {
//     "name": "Dell 27-inch 4K Monitor",
//     "avgRating": 4
//   },
//   {
//     "name": "OnePlus Nord CE 3",
//     "avgRating": 4
//   },
//   {
//     "name": "Samsung 55-inch QLED TV",
//     "avgRating": 4.5
//   },
//   {
//     "name": "Levi's 511 Slim Fit Jeans",
//     "avgRating": 4.666666666666667
//   },
//   {
//     "name": "Nike Air Max 270 Sneakers",
//     "avgRating": 4.5
//   },
//   {
//     "name": "Adidas Originals T-Shirt",
//     "avgRating": 4.333333333333333
//   },
//   {
//     "name": "Puma RS-X Sneakers",
//     "avgRating": 4.5
//   },
//   {
//     "name": "Reebok Training Trackpants",
//     "avgRating": 4.5
//   }
// ]

//Operation 4: Update Operation (2 marks)
// Add a new review to product "ELEC001"
// Review: {user: "U999", rating: 4, comment: "Good value", date: ISODate()}
db.products.updateOne(
  { product_id: "ELEC001" },
  {
    $push: {
      reviews: {
        user: "U999",
        rating: 4,
        comment: "Good value",
        date: ISODate()
      }
    }
  }
)
// Output
// {
//   "acknowledged": true,
//   "insertedId": null,
//   "matchedCount": 1,
//   "modifiedCount": 1,
//   "upsertedCount": 0
// }

//Operation 5: Complex Aggregation (3 marks)
// Calculate average price by category
// Return: category, avg_price, product_count
// Sort by avg_price descending

db.products.aggregate([
  {
    $group: {
      _id: "$category",
      avg_price: { $avg: "$price" },
      product_count: { $sum: 1 }
    }
  },
  {
    $project: {
      category: "$_id",
      avg_price: 1,
      product_count: 1,
      _id: 0
    }
  },
  {
    $sort: {
      avg_price: -1
    }
  }
])
// Output 
// [
//   {
//     "avg_price": 70830.83333333333,
//     "product_count": 6,
//     "category": "Electronics"
//   },
//   {
//     "avg_price": 5215,
//     "product_count": 6,
//     "category": "Fashion"
//   }
// ]