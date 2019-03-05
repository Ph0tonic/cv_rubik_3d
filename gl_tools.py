import moderngl


def create_context():
    return moderngl.create_context()


def create_vertices_buffer(vertices):
    vBuffer = glBuffer(GL_ARRAY_BUFFER, len(vertices), vertices, GL_STATIC_DRAW)


def create_indices_buffer():
    None


def create_colors_buffer():
    None


def load_shaders(context, vertex_shader_filepath, fragment_shader_filepath):
    vertex_shader = load_file_content(vertex_shader_filepath)
    fragment_shader = load_file_content(fragment_shader_filepath)
    return context.program(vertex_shader = vertex_shader, fragment_shader = fragment_shader)


def load_file_content(filepath):
    file = open(filepath, 'r')
    content = file.read()
    file.close()
    return content
