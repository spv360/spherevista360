<?php
/**
 * Functions and definitions
 */

function spherevista360_safe_setup() {
    // Add theme support
    add_theme_support( 'title-tag' );
    add_theme_support( 'post-thumbnails' );
    add_theme_support( 'automatic-feed-links' );
    add_theme_support( 'html5', array( 'comment-list', 'comment-form', 'search-form' ) );
}
add_action( 'after_setup_theme', 'spherevista360_safe_setup' );

function spherevista360_safe_scripts() {
    wp_enqueue_style( 'spherevista360-safe-style', get_stylesheet_uri(), array(), '1.0' );
}
add_action( 'wp_enqueue_scripts', 'spherevista360_safe_scripts' );
