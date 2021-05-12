(define (domain SimpleSatellite)

    (:requirements
        :durative-actions
        :equality
        :negative-preconditions
        :numeric-fluents
        :object-fluents
        :typing
    )

    (:types
        image
        memory
    )

    (:predicates
        (image_available ?i  - image)
        (image_dumped ?i  - image)
        
        (memory_free ?m - memory)
        (memory_taken ?m - memory ?i - image)
        (image_analysed ?m - memory ?i  - image)
        
        (dump_available)
        
        (sat_busy)
        (sat_free)
    )

    (:functions
        (image_score ?i - image)
        (total_score)
    )

    (:durative-action take_image
        :parameters (?i - image ?m - memory)
        :duration (= ?duration 3)
        :condition (and 
            (at start (sat_free))
            (at start (image_available ?i))
            (at start (memory_free ?m))
            )
        :effect (and
            (at start (not (sat_free)))
            (at start (sat_busy))
            (at start (not (memory_free ?m)))
            (at end (memory_taken ?m ?i))
            (at end (not (sat_busy)))
            (at end (sat_free))
            )
    )
    
    (:durative-action analyse_image
        :parameters (?i - image ?m - memory)
        :duration (= ?duration 50)
        :condition (and 
            (at start (sat_free))
            (at start (memory_taken ?m ?i))
            )
        :effect (and
            (at start (not (sat_free)))
            (at start (sat_busy))
            (at end (image_analysed ?m ?i))
            (at end (not (sat_busy)))
            (at end (sat_free))
            )
    )
    
    (:durative-action dump_image
        :parameters (?i - image ?m - memory)
        :duration (= ?duration 20)
        :condition (and 
            (at start (sat_free))
            (at start (image_analysed ?m ?i))
            (at start (dump_available))
            )
        :effect (and
            (at start (not (sat_free)))
            (at start (sat_busy))
            (at start (not (memory_taken ?m ?i)))
            (at end (memory_free ?m))
            (at end (image_dumped ?i))
            (at end (not (sat_busy)))
            (at end (sat_free))
            (at end (increase (total_score) (image_score ?i)))
            )
    )
)