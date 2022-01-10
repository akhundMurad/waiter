def test_add_table(restaurant_repo, restaurant, test_client):
    restaurant_repo.add(restaurant)
    restaurant_repo.session.commit()

    response = test_client.post(f'/restaurant/{restaurant.id}/table/')

    assert response.status_code == 201
    assert response.json()['index'] == 1


def test_create_menu_item(restaurant_repo, restaurant, test_client):
    restaurant_repo.add(restaurant)
    restaurant_repo.session.commit()

    data = {
        'title': 'title',
        'description': 'description',
        'price': 2.0
    }

    response = test_client.post(
        f'/restaurant/{restaurant.id}/menu-item/', json=data
    )

    assert response.status_code == 201


def test_make_order(restaurant_repo, menu_item, test_client):
    table = menu_item.restaurant.add_table()
    restaurant_repo.add(menu_item.restaurant)
    restaurant_repo.session.commit()

    data = {
        'table': table.index,
        'order_mapping': [
            {'menu_item': str(menu_item.id), 'quantity': 1}
        ]
    }

    response = test_client.post(
        f'/restaurant/{menu_item.restaurant.id}/order/', json=data
    )

    assert response.status_code == 201
