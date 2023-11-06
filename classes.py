import time




class AnimauxMarins:

    def __init__(self, seconds, repetitions):
        self.seconds = seconds
        self.repetitions = repetitions



    def timer(seconds, repetitions):

        repetitions = 0
        chronon_count = 0

        while repetitions < 7:
            start_time = time.time()
            end_time = start_time + seconds

            while time.time() < end_time:
                remaining_time = int(end_time - time.time())
                print(f"Jours passés : {chronon_count}, Temps restant : {remaining_time} secondes", end='\r')
                time.sleep(1)  # Attendez 1 seconde avant de vérifier à nouveau le temps

        print("Un nouveau jour est passé !")
        chronon_count += 1
        repetitions += 1
        print(f"Jours passés : {chronon_count}")

        # Utilisation du timer pendant 20 secondes (1 jour)
    timer(20, 7)
