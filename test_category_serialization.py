
from domain.category import Category

def test_category_serialization():
    original_category = Category(
        name="Eletrônicos",
        description="Produtos eletrônicos em geral",
        is_active=True
    )
    print(f"Original: {original_category}")

    serialized_data = original_category.to_dict()
    print(f"Serializado: {serialized_data}")

    reconstructed_category = Category.from_dict(serialized_data)
    print(f"Reconstruído: {reconstructed_category}")

    assert original_category == reconstructed_category
    assert original_category.name == reconstructed_category.name
    assert original_category.description == reconstructed_category.description
    assert original_category.is_active == reconstructed_category.is_active
    print("Teste de serialização e desserialização da Categoria: SUCESSO!")

if __name__ == "__main__":
    test_category_serialization()

