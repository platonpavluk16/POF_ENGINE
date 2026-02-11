import glfw
from OpenGL.GL import *
import ctypes
from .camera import Camera

VERTEX_SRC = """
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;
uniform mat4 uModel; uniform mat4 uView; uniform mat4 uProj;
out vec2 TexCoord;
void main() {
    gl_Position = uProj * uView * uModel * vec4(aPos, 1.0);
    TexCoord = aTexCoord;
}
"""

FRAGMENT_SRC = """
#version 330 core
in vec2 TexCoord;
out vec4 FragColor;
uniform vec4 uColor;
uniform sampler2D uTexture;
uniform bool uUseTexture;
void main() {
    if (uUseTexture) FragColor = texture(uTexture, TexCoord) * uColor;
    else FragColor = uColor;
}
"""


class Engine:
    def __init__(self, width, height, title):
        if not glfw.init(): raise Exception("GLFW Error")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        self.window = glfw.create_window(width, height, title, None, None)
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)

        glEnable(GL_DEPTH_TEST)  # Щоб 3D об'єкти не були прозорими
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.program = self._create_prog(VERTEX_SRC, FRAGMENT_SRC)
        self.camera = Camera(width, height)
        self.renderables = []
        self.last_time = glfw.get_time()

        # Реєструємо функцію зміни розміру
        glfw.set_framebuffer_size_callback(self.window, self._on_resize)

    def _on_resize(self, window, width, height):
        glViewport(0, 0, width, height)
        if hasattr(self, 'camera'):
            self.camera.width = width
            self.camera.height = height

    def _create_prog(self, vs_s, fs_s):
        def comp(s, t):
            sh = glCreateShader(t);
            glShaderSource(sh, s);
            glCompileShader(sh)
            if not glGetShaderiv(sh, GL_COMPILE_STATUS):
                raise Exception(f"Shader: {glGetShaderInfoLog(sh)}")
            return sh

        vs = comp(vs_s, GL_VERTEX_SHADER);
        fs = comp(fs_s, GL_FRAGMENT_SHADER)
        p = glCreateProgram();
        glAttachShader(p, vs);
        glAttachShader(p, fs);
        glLinkProgram(p)
        return p

    def _upload_render(self, r):
        vao = glGenVertexArrays(1);
        vbo = glGenBuffers(1)
        glBindVertexArray(vao);
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        verts = (ctypes.c_float * len(r.vertex_data))(*r.vertex_data)
        glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(verts), verts, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        ebo = None;
        count = len(r.vertex_data) // 3
        if r.indices:
            ebo = glGenBuffers(1);
            inds = (ctypes.c_uint * len(r.indices))(*r.indices)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, ctypes.sizeof(inds), inds, GL_STATIC_DRAW)
            count = len(r.indices)
        r._gpu = (vao, vbo, ebo, count)

    def add_render(self, render):
        self._upload_render(render)
        self.renderables.append(render)

    def begin(self):
        glfw.poll_events()
        t = glfw.get_time();
        dt = t - self.last_time;
        self.last_time = t

        # ЛОГІКА ОБЕРТАННЯ
        for r in self.renderables:
            if hasattr(r, 'owner') and r.owner:
                r.owner.apply_components()
                rot = r.owner.components.get("rotation")
                if rot and rot.get("enabled", True):
                    r.transform.rotation_x += float(rot.get("speed_x", 0.0)) * dt
                    r.transform.rotation_y += float(rot.get("speed_y", 0.0)) * dt
                    r.transform.rotation_z += float(rot.get("speed_z", 0.0)) * dt

                    t_comp = r.owner.components["transform"]
                    t_comp["rotation_x"], t_comp["rotation_y"], t_comp["rotation_z"] = \
                        r.transform.rotation_x, r.transform.rotation_y, r.transform.rotation_z

        self.camera.update()
        self.view = self.camera.get_view_matrix()
        self.proj = self.camera.get_projection_matrix()
        glClearColor(0.1, 0.1, 0.12, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def draw(self):
        glUseProgram(self.program)
        glUniformMatrix4fv(glGetUniformLocation(self.program, "uView"), 1, GL_FALSE, self.view)
        glUniformMatrix4fv(glGetUniformLocation(self.program, "uProj"), 1, GL_FALSE, self.proj)

        for r in self.renderables:
            model = r.transform.to_mat4()
            glUniformMatrix4fv(glGetUniformLocation(self.program, "uModel"), 1, GL_FALSE, model)
            glUniform4f(glGetUniformLocation(self.program, "uColor"), *r.color)

            vao, _, ebo, count = r._gpu
            glBindVertexArray(vao)
            if ebo:
                glDrawElements(GL_TRIANGLES, count, GL_UNSIGNED_INT, None)
            else:
                glDrawArrays(GL_TRIANGLES, 0, count)

    def end(self):
        glfw.swap_buffers(self.window)

    def should_close(self):
        return glfw.window_should_close(self.window)

    def terminate(self):
        if hasattr(self, 'program'):
            glDeleteProgram(self.program)

        for r in self.renderables:
            if hasattr(r, '_gpu') and r._gpu:
                vao, vbo, ebo, _ = r._gpu
                glDeleteVertexArrays(1, [vao])
                glDeleteBuffers(1, [vbo])
                if ebo:
                    glDeleteBuffers(1, [ebo])

        # Закриваємо GLFW
        glfw.terminate()