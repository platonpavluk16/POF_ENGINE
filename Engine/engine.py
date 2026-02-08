import glfw
from OpenGL.GL import *
import ctypes
from .camera import Camera

VERTEX_SRC = """
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;

uniform mat4 uModel;
uniform mat4 uView;
uniform mat4 uProj;

out vec2 TexCoord;
out vec2 LocalPos;

void main() {
    gl_Position = uProj * uView * uModel * vec4(aPos, 1.0);
    TexCoord = aTexCoord;
    LocalPos = aPos.xy;
}
"""

FRAGMENT_SRC = """
#version 330 core
in vec2 TexCoord;
in vec2 LocalPos;
out vec4 FragColor;

uniform vec4 uColor;
uniform sampler2D uTexture;
uniform bool uUseTexture;
uniform int uShapeType;
uniform float uRadius;
uniform float uWidth;
uniform float uHeight;

bool isInCircle() {
    float dist = length(LocalPos);
    return dist <= uRadius;
}

bool isInRectangle() {
    return abs(LocalPos.x) <= uWidth / 2.0 && abs(LocalPos.y) <= uHeight / 2.0;
}

bool isInTriangle() {
    float h = uHeight / 2.0;
    float w = uWidth / 2.0;
    
    if (LocalPos.y < -h) return false;
    
    float y_from_base = LocalPos.y + h;
    float width_at_y = w * (1.0 - (y_from_base / (2.0 * h)));
    
    return abs(LocalPos.x) <= width_at_y;
}

void main() {
    bool inShape = false;
    
    if (uShapeType == 0) {
        inShape = isInCircle();
    } else if (uShapeType == 1) {
        inShape = isInRectangle();
    } else if (uShapeType == 2) {
        inShape = isInTriangle();
    }
    
    if (!inShape) {
        discard;
    }
    
    if (uUseTexture) {
        FragColor = texture(uTexture, TexCoord) * uColor;
    } else {
        FragColor = uColor;
    }
}
"""

def compile_shader(src, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, src)
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        info = glGetShaderInfoLog(shader).decode()
        raise RuntimeError(info)
    return shader

def create_program(vs_src, fs_src):
    vs = compile_shader(vs_src, GL_VERTEX_SHADER)
    fs = compile_shader(fs_src, GL_FRAGMENT_SHADER)
    prog = glCreateProgram()
    glAttachShader(prog, vs)
    glAttachShader(prog, fs)
    glLinkProgram(prog)
    if not glGetProgramiv(prog, GL_LINK_STATUS):
        info = glGetProgramInfoLog(prog).decode()
        raise RuntimeError(info)
    glDeleteShader(vs)
    glDeleteShader(fs)
    return prog

class Engine:
    def __init__(self, width, height, title):
        if not glfw.init():
            raise Exception("Failed to initialize GLFW")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("Failed to create GLFW window")

        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        glfw.set_framebuffer_size_callback(self.window, self._on_resize)

        self.program = create_program(VERTEX_SRC, FRAGMENT_SRC)
        self.uModel = glGetUniformLocation(self.program, "uModel")
        self.uView = glGetUniformLocation(self.program, "uView")
        self.uProj = glGetUniformLocation(self.program, "uProj")
        self.uColor = glGetUniformLocation(self.program, "uColor")

        self.identity = [
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0,
        ]

        self.camera = Camera(width, height)
        self.view = self.camera.get_view_matrix()
        self.proj = self.camera.get_projection_matrix()
        self.renderables = []

        w, h = glfw.get_framebuffer_size(self.window)
        self._on_resize(self.window, w, h)

    def _on_resize(self, window, width, height):
        glViewport(0, 0, width, height)

    def _clear_gpu(self, render):
        if render._gpu is not None:
            vao, vbo, ebo, _ = render._gpu
            glDeleteVertexArrays(1, [vao])
            glDeleteBuffers(1, [vbo])
            if ebo is not None:
                glDeleteBuffers(1, [ebo])
            render._gpu = None

    def _upload_render(self, render):
        self._clear_gpu(render)
        
        if render.sprite:
            vertex_data = render.sprite.get_quad_vertices(render.sprite.width, render.sprite.height)
            uv_data = render.sprite.get_quad_uv()
            
            combined_data = []
            for i in range(len(vertex_data) // 3):
                combined_data.extend([vertex_data[i*3], vertex_data[i*3+1], vertex_data[i*3+2]])
                combined_data.extend([uv_data[i*2], uv_data[i*2+1]])
            
            vao = glGenVertexArrays(1)
            vbo = glGenBuffers(1)
            
            glBindVertexArray(vao)
            glBindBuffer(GL_ARRAY_BUFFER, vbo)
            
            verts = (ctypes.c_float * len(combined_data))(*combined_data)
            glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(verts), verts, GL_STATIC_DRAW)
            
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0))
            glEnableVertexAttribArray(0)
            
            glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))
            glEnableVertexAttribArray(1)
            
            ebo = glGenBuffers(1)
            indices = render.sprite.get_quad_indices()
            inds = (ctypes.c_uint * len(indices))(*indices)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, ctypes.sizeof(inds), inds, GL_STATIC_DRAW)
            
            glBindVertexArray(0)
            render._gpu = (vao, vbo, ebo, len(indices))
        
        elif not render.vertex_data:
            raise ValueError("Render has no vertex data")
        
        else:
            vao = glGenVertexArrays(1)
            vbo = glGenBuffers(1)

            glBindVertexArray(vao)
            glBindBuffer(GL_ARRAY_BUFFER, vbo)

            verts = (ctypes.c_float * len(render.vertex_data))(*render.vertex_data)
            glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(verts), verts, GL_STATIC_DRAW)

            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0))
            glEnableVertexAttribArray(0)

            ebo = None
            index_count = 0

            if render.indices:
                ebo = glGenBuffers(1)
                inds = (ctypes.c_uint * len(render.indices))(*render.indices)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
                glBufferData(GL_ELEMENT_ARRAY_BUFFER, ctypes.sizeof(inds), inds, GL_STATIC_DRAW)
                index_count = len(render.indices)
            else:
                index_count = len(render.vertex_data) // 3

            glBindVertexArray(0)

            render._gpu = (vao, vbo, ebo, index_count)

    def add_render(self, render):
        if render._gpu is None:
            self._upload_render(render)
        self.renderables.append(render)

    def remove_render(self, render):
        if render in self.renderables:
            self._clear_gpu(render)
            self.renderables.remove(render)

    def begin(self):
        glfw.poll_events()
        self.update_scripts()
        self.update_collisions()
        self.camera.update()
        self.view = self.camera.get_view_matrix()
        self.proj = self.camera.get_projection_matrix()
        glClearColor(0.05, 0.05, 0.08, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

    def update_scripts(self):
        for render in self.renderables:
            if hasattr(render, "scripts") and render.scripts:
                for script in render.scripts:
                    script.on_update()

    def check_aabb_collision(self, pos1_x, pos1_y, size1_w, size1_h, scale1,
                         pos2_x, pos2_y, size2_w, size2_h, scale2):
        w1 = (size1_w * scale1) / 2
        h1 = (size1_h * scale1) / 2
        w2 = (size2_w * scale2) / 2
        h2 = (size2_h * scale2) / 2
        
        return not (pos1_x + w1 < pos2_x - w2 or
                    pos1_x - w1 > pos2_x + w2 or
                    pos1_y + h1 < pos2_y - h2 or
                    pos1_y - h1 > pos2_y + h2)

    def resolve_collision(self, render1, render2):
        if not render1.collider.is_solid or not render2.collider.is_solid:
            return
        
        dx = render1.transform.x - render2.transform.x
        dy = render1.transform.y - render2.transform.y

        distance = (dx*dx + dy*dy) ** 0.5
        if distance < 0.01:
            distance = 0.01

        dx /= distance
        dy /= distance

        m1 = render1.collider.mass
        m2 = render2.collider.mass
        total_mass = m1 + m2
        
        separation = 0.05
        render1.transform.x += dx * separation * (m2 / total_mass)
        render1.transform.y += dy * separation * (m2 / total_mass)
        render2.transform.x -= dx * separation * (m1 / total_mass)
        render2.transform.y -= dy * separation * (m1 / total_mass)

    def update_collisions(self):
        for i, render1 in enumerate(self.renderables):
            if render1.collider:
                render1.collider.colliding_with = []

        for i, render1 in enumerate(self.renderables):
            if not render1.collider:
                continue

            for j in range(i + 1, len(self.renderables)):
                render2 = self.renderables[j]
                if not render2.collider:
                    continue
                
                colliding = self.check_aabb_collision(
                    render1.transform.x, render1.transform.y,
                    render1.collider.width, render1.collider.height,
                    render1.transform.scale,
                    render2.transform.x, render2.transform.y,
                    render2.collider.width, render2.collider.height,
                    render2.transform.scale
                )
                
                if colliding:
                    render1.collider.colliding_with.append(render2)
                    render2.collider.colliding_with.append(render1)
                    self.resolve_collision(render1, render2)
                    
                    if hasattr(render1, "scripts") and render1.scripts:
                        for script in render1.scripts:
                            script.on_collision(render2)
                    if hasattr(render2, "scripts") and render2.scripts:
                        for script in render2.scripts:
                            script.on_collision(render1)

    def draw(self):
        glUseProgram(self.program)
        glUniformMatrix4fv(self.uView, 1, GL_FALSE, self.view)
        glUniformMatrix4fv(self.uProj, 1, GL_FALSE, self.proj)

        for render in self.renderables:
            if render._gpu is None:
                self._upload_render(render)

            vao, vbo, ebo, count = render._gpu
            model = render.transform.to_mat4() if render.transform else self.identity
            glUniformMatrix4fv(self.uModel, 1, GL_FALSE, model)

            color = render.color
            if len(color) == 3:
                color = (color[0], color[1], color[2], 1.0)
            glUniform4f(self.uColor, color[0], color[1], color[2], color[3])

            shape_type = 1
            radius = 0.5
            width = 1.0
            height = 1.0
            
            if render.sprite:
                glUniform1i(glGetUniformLocation(self.program, "uUseTexture"), 1)
                glActiveTexture(GL_TEXTURE0)
                glBindTexture(GL_TEXTURE_2D, render.sprite.texture_id)
                glUniform1i(glGetUniformLocation(self.program, "uTexture"), 0)
            else:
                glUniform1i(glGetUniformLocation(self.program, "uUseTexture"), 0)
            
            if render.shape:
                shape_name = render.shape.__class__.__name__.lower()
                if "circle" in shape_name:
                    shape_type = 0
                    radius = render.shape.radius if hasattr(render.shape, 'radius') else 0.5
                elif "triangle" in shape_name:
                    shape_type = 2
                    if hasattr(render.shape, 'width'):
                        width = render.shape.width
                    if hasattr(render.shape, 'height'):
                        height = render.shape.height
                else:
                    shape_type = 1
                    if hasattr(render.shape, 'width'):
                        width = render.shape.width
                    if hasattr(render.shape, 'height'):
                        height = render.shape.height
            
            glUniform1i(glGetUniformLocation(self.program, "uShapeType"), shape_type)
            glUniform1f(glGetUniformLocation(self.program, "uRadius"), radius)
            glUniform1f(glGetUniformLocation(self.program, "uWidth"), width)
            glUniform1f(glGetUniformLocation(self.program, "uHeight"), height)

            glBindVertexArray(vao)
            mode = GL_LINES if render.draw_mode == "lines" else GL_TRIANGLES

            if ebo is not None:
                glDrawElements(mode, count, GL_UNSIGNED_INT, None)
            else:
                glDrawArrays(mode, 0, count)

        glBindVertexArray(0)

    def should_close(self):
        return glfw.window_should_close(self.window)

    def end(self):
        glfw.swap_buffers(self.window)

    def terminate(self):
        for render in self.renderables:
            self._clear_gpu(render)

        glDeleteProgram(self.program)
        glfw.terminate()
