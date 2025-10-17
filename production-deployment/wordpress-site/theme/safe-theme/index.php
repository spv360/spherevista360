<?php get_header(); ?>

<div class="content-wrapper">
    <?php
    if ( have_posts() ) :
        while ( have_posts() ) : the_post();
            ?>
            <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
                <h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
                
                <?php if ( has_post_thumbnail() ) : ?>
                    <div class="post-thumbnail">
                        <a href="<?php the_permalink(); ?>">
                            <?php the_post_thumbnail( 'medium' ); ?>
                        </a>
                    </div>
                <?php endif; ?>
                
                <div class="entry-excerpt">
                    <?php the_excerpt(); ?>
                </div>
                
                <a href="<?php the_permalink(); ?>">Read More →</a>
            </article>
            <?php
        endwhile;
        
        the_posts_navigation();
    else :
        ?>
        <p>No posts found.</p>
        <?php
    endif;
    ?>
</div>

<?php get_footer(); ?>
