(require 'asdf)

;; Add the CL Domain directory to the registry
(push (make-pathname
       :directory (pathname-directory (truename (uiop:current-lisp-file-pathname))))
      asdf:*central-registry*)

(let ((quicklisp-init (find-if
                       (lambda (path)
                         (probe-file
                          (merge-pathnames path (user-homedir-pathname))))
                       '("quicklisp/setup.lisp" ".quicklisp/setup.lisp"))))
  (when quicklisp-init
    (load (merge-pathnames quicklisp-init (user-homedir-pathname)))))

(ql:quickload 'sphinxcontrib.cldomain :silent t)

(load (make-pathname
       :directory (pathname-directory (truename (uiop:current-lisp-file-pathname)))
       :name "cli" :type "lisp"))

(apply #'sphinxcontrib.cldomain.cli:main (uiop:command-line-arguments))
