<?php get_header(); ?>

<div class="content-wrapper">
    <?php
    if ( have_posts() ) :
        while ( have_posts() ) : the_post();
            ?>
            <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
                <header class="entry-header">
                    <h1 class="entry-title"><?php the_title(); ?></h1>
                    <div class="entry-meta">
                        Posted on <?php echo get_the_date(); ?>
                    </div>
                </header>

                <?php if ( has_post_thumbnail() ) : ?>
                    <div class="post-thumbnail">
                        <?php the_post_thumbnail( 'large' ); ?>
                    </div>
                <?php endif; ?>

                <div class="entry-content">
                    <?php the_content(); ?>
                </div>
            </article>

            <?php
            // WordPress will use default comments if we don't include comments_template()
            // This is SAFER - no custom code to break
            if ( comments_open() || get_comments_number() ) :
                comments_template();
            endif;
            ?>
            
            <?php
        endwhile;
    endif;
    ?>
</div>

<?php get_footer(); ?>
