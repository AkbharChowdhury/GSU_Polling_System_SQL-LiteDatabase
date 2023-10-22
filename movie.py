class Movie:
    @staticmethod
    def columns():
        return [
            'Movie',
            'Duration',
            'Rating',
            'Genre'
        ]

    @staticmethod
    def get_data():
        return (
            ("Spiderman 3", "2:20", "15", "Action"),
            ("Child's Play ", "90:00", "18", "Horror/Thriller"),

        )
    @staticmethod
    def get_movie_data():
        return {
            'movie': {
                'title': "Spiderman 3",
                'duration': 220,
                'rating': '15',
                'genres': ['Action']
            },
            'movie2': {
                'title': "Child's Play",
                'duration': 90,
                'rating': '18',
                'genres': ['Horror', 'Thriller']
            }
        }
