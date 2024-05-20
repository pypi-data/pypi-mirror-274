(defpackage :sphinxcontrib.cldomain.cli
  (:use :cl :sphinxcontrib.cldomain)
  (:export #:main))
(in-package :sphinxcontrib.cldomain.cli)

(defun main (&rest argv)
  "Entry point for our application."
  (opts:define-opts
      (:name :help
       :description "print this help text"
       :short #\h
       :long "help")
      (:name :packages
       :description "The packages to document."
       :long "packages"
       :arg-parser #'identity)
    (:name :systems
     :description "The system to load."
     :long "systems"
     :arg-parser #'identity)
    (:name :paths
     :description "Extra paths to search fro ASDF systems."
     :long "paths"
     :arg-parser #'identity))

  (multiple-value-bind (options free-args)
      (opts:get-opts argv)
    (declare (ignorable free-args))
    (if (getf options :help)
        (opts:describe
         :prefix "export symbols from a LISP program for documentation"
         :usage-of "./cldomain.ros"))
    (if (getf options :paths)
        (dolist (path (uiop:split-string (getf options :paths) :separator '(#\,)))
          (let ((path-pathname (pathname path)))
            ;; CLISP's truename spews if path is a directory, whereas ext:probe-filename
            ;; will generate a directory-truename for directories without spewing...???
            #+clisp
            (let ((dir-truename (ext:probe-pathname path)))
              (when dir-truename
                (push  dir-truename asdf:*central-registry*)))
            #-(or clisp)
            (push (truename path-pathname) asdf:*central-registry*))))
    (if (getf options :systems)
        (let ((*standard-output* *error-output*)
              (*debug-io* *error-output*)
              (*trace-output* *error-output*))
          (dolist (system (uiop:split-string (getf options :systems) :separator '(#\,)))
            ;; TODO this should fall back to use ASDF load-ops, that
            ;; would make it support systems that don't have quicklisp
            (ql:quickload system :prompt nil))))
    (princ
     (apply #'render-result (uiop:split-string (getf options :packages) :separator '(#\,))))))
