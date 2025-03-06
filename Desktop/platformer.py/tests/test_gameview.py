import arcade

from gameview import GameView

INITIAL_COIN_COUNT = 5

def test_collect_coins(window: arcade.Window) -> None:
    view = GameView()
    window.show_view(view)

    # Make sure we have the amount of coins we expect at the start
    assert len(view.coin_list) == INITIAL_COIN_COUNT

    # Start moving right
    view.on_key_press(arcade.key.RIGHT, 0)

    # Let the game run for 1 second
    window.test(60)

    # We should have collected the first coin
    assert len(view.coin_list) == INITIAL_COIN_COUNT - 1

    # Jump to get past the first crate
    view.on_key_press(arcade.key.UP, 0)
    view.on_key_release(arcade.key.UP, 0)

    # Let the game run for 1 more second
    window.test(60)

    # We should have collected the second coin
    assert len(view.coin_list) == INITIAL_COIN_COUNT - 2

    # test que la topuche echap pour reset le jeu fonctionne bien

    def test_reset_with_escape(window: arcade.Window) -> None:
        view = GameView()
        window.show_view(view)

        # le joueur se déplace
        view.player_sprite.center_x += 200

        # Appuyer sur ECHAP pour réinitialiser
        view.on_key_press(arcade.key.ESCAPE, 0)

        # Vérifier que le joueur est revenu à sa position initiale
        assert view.player_sprite.center_x == 64
        assert view.player_sprite.center_y == 128