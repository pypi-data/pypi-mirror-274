import sys

import matplotlib.pyplot as plt
import numpy as np
import scipy.spatial

import delaunay_triangulation_and_its_dual_2d
import delaunay_triangulation_and_its_dual_2d.exceptions
import delaunay_triangulation_and_its_dual_2d.geometry


def visualize_mocked_scipy_spatial_delaunay_and_voronoi():
    points = np.array(
        [[0, 0], [3, 0], [1, 1], [3, 2], [4, 2], [1, 3], [2, 4], [4, 4]],
        dtype=np.float32,
    )
    delaunay = delaunay_triangulation_and_its_dual_2d.Delaunay(points=points)
    delaunay_diagram = delaunay.get_mocked_scipy_spatial_delaunay()
    fig = scipy.spatial.delaunay_plot_2d(delaunay_diagram)
    barycentric_dual_diagram = (
        delaunay.get_barycentric_dual_as_mocked_scipy_spatial_voronoi()
    )
    fig = scipy.spatial.voronoi_plot_2d(
        barycentric_dual_diagram, ax=fig.axes[0]
    )
    voronoi_diagram = delaunay.get_mocked_scipy_spatial_voronoi()
    fig = scipy.spatial.voronoi_plot_2d(voronoi_diagram, ax=fig.axes[0])
    fig.axes[0].set_xlim(-2, 6)
    fig.axes[0].set_ylim(-2, 6)
    plt.grid()
    plt.show()


def try_compute_bounded_line_segments_of_dual_from_predefined_points():
    points = np.array(
        [[0, 0], [3, 0], [1, 1], [3, 2], [4, 2], [1, 3], [2, 4], [4, 4]],
        dtype=np.float32,
    )
    delaunay = delaunay_triangulation_and_its_dual_2d.Delaunay(points=points)
    bounded_line_segments = delaunay.compute_bounded_line_segments_of_dual(
        dual="voronoi"
    )
    print("bounded_line_segments.shape: ", bounded_line_segments.shape)


def try_compute_bounded_line_segments_of_dual_from_random_points():
    lower_bound = 0.0
    upper_bound = 1.0
    rng = np.random.default_rng()
    points = rng.uniform(low=lower_bound, high=upper_bound, size=(20, 2))
    delaunay = delaunay_triangulation_and_its_dual_2d.Delaunay(
        points=points,
        bounding_box=delaunay_triangulation_and_its_dual_2d.geometry.BoundingBox2d(
            min_=np.array([lower_bound, lower_bound], dtype=np.float_),
            max_=np.array([upper_bound, upper_bound], dtype=np.float_),
        ),
    )
    bounded_line_segments = delaunay.compute_bounded_line_segments_of_dual(
        # dual="voronoi"
        dual="barycentric"
    )
    valid_ridge_vertices_mask = np.all(
        ~np.isnan(bounded_line_segments), axis=(1, 2)
    )
    print(bounded_line_segments)
    print(np.array(delaunay.ridge_vertices))
    print(np.count_nonzero(~valid_ridge_vertices_mask))
    # print("bounded_line_segments.shape: ", bounded_line_segments.shape)


def find_exception_by_creating_random_graphs() -> None:
    lower_bound = 0.0
    upper_bound = 1000.0
    rng = np.random.default_rng()
    for i in range(1000):
        print("i: ", i)
        points = rng.uniform(low=lower_bound, high=upper_bound, size=(20, 2))
        for _ in range(2):
            points = delaunay_triangulation_and_its_dual_2d.Delaunay.voronoi_iteration(
                points=points, rng=rng
            )
        delaunay = delaunay_triangulation_and_its_dual_2d.Delaunay(
            points=points,
            bounding_box=delaunay_triangulation_and_its_dual_2d.geometry.BoundingBox2d(
                min_=np.array([lower_bound, lower_bound], dtype=np.float_),
                max_=np.array([upper_bound, upper_bound], dtype=np.float_),
            ),
        )
        bounded_line_segments = delaunay.compute_bounded_line_segments_of_dual(
            # dual="voronoi"
            dual="barycentric"
        )
        valid_ridge_vertices_mask = np.all(
            ~np.isnan(bounded_line_segments), axis=(1, 2)
        )
        if __debug__:
            if np.count_nonzero(~valid_ridge_vertices_mask) == 0:
                continue
            barycentric_dual_diagram = (
                delaunay.get_barycentric_dual_as_mocked_scipy_spatial_voronoi()
            )
            fig = scipy.spatial.voronoi_plot_2d(barycentric_dual_diagram)
            for vertices, coordinates in zip(
                delaunay.ridge_vertices, bounded_line_segments
            ):
                fig.axes[0].text(
                    *coordinates[0].tolist(), s=str(vertices[0]), fontsize=9
                )
                fig.axes[0].text(
                    *coordinates[1].tolist(), s=str(vertices[1]), fontsize=9
                )
            fig.axes[0].set_xlim(lower_bound - 1, upper_bound + 1)
            fig.axes[0].set_ylim(lower_bound - 1, upper_bound + 1)
            plt.grid()
            plt.show()


def examine_liang_barsky_line_clipping() -> None:
    bounding_box = (
        delaunay_triangulation_and_its_dual_2d.geometry.BoundingBox2d(
            min_=np.array([0.0, 0.0], dtype=np.float_),
            max_=np.array([1000.0, 1000.0], dtype=np.float_),
        )
    )
    line_segments = np.array(
        [[[846.33138538, 149.42700369], [763.7151303, 149.42700369]]],
        dtype=np.float_,
    )
    result = bounding_box.liang_barsky_line_clipping(
        line_segments=line_segments
    )


if __name__ == "__main__":
    # Reference: https://stackoverflow.com/a/52837375
    globals()[sys.argv[1]]()
